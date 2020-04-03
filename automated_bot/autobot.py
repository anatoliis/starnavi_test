import argparse
import os
import random
import time
from configparser import ConfigParser
from functools import partial
from itertools import islice
from typing import Any, Dict, Tuple
from typing import Callable, Generator, List

from tqdm.contrib.concurrent import thread_map

from api_client import APIClient, User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, "autobot.ini")
DEFAULT_API_URL = "http://127.0.0.1:80/api/"

SETTINGS_FIELDS = {
    "number_of_users": int,
    "max_posts_per_user": int,
    "max_likes_per_user": int,
}


def main():
    arguments = parse_arguments()
    settings = parse_config(arguments["config"])
    client = APIClient(arguments["url"])

    print("Creating Users..")

    users = execute_in_threads(
        func=partial(create_user, client),
        sequence=({"user_index": i} for i in range(settings["number_of_users"])),
        max_sequence_length=settings["number_of_users"],
    )

    print("Creating Posts for each User..")

    number_of_posts_for_each_user = [
        random.randint(0, settings["max_posts_per_user"]) for _ in range(len(users))
    ]
    total_number_of_posts = sum(number_of_posts_for_each_user)

    post_ids = execute_in_threads(
        func=partial(create_post, client),
        sequence=post_authors_generator(users, number_of_posts_for_each_user),
        max_sequence_length=total_number_of_posts,
    )

    print("Liking random Posts by each User..")

    number_of_likes_for_each_user = [
        random.randint(0, min(settings["max_likes_per_user"], len(post_ids)))
        for _ in range(len(users))
    ]
    total_number_of_likes = sum(number_of_likes_for_each_user)

    execute_in_threads(
        func=partial(like_post, client),
        sequence=posts_to_like_generator(
            users, post_ids, number_of_likes_for_each_user
        ),
        max_sequence_length=total_number_of_likes,
    )

    print(
        f"\nTotal Users created: {len(users)}\n"
        f"Total Posts created: {total_number_of_posts}\n"
        f"Total number of Likes: {total_number_of_likes}"
    )


def execute_in_threads(
    func: Callable, sequence: Generator, max_sequence_length: int,
) -> List:
    """Executing 'func' in ThreadPoolExecutor for each
    set of arguments received from 'sequence' generator

    :param func: Callable to be executed in ThreadPoolExecutor.
    :param sequence: A generator yielding sets of arguments
    that are passed to 'func' on each call.
    :param max_sequence_length: Limits maximum number of 'func' calls in
    order to avoid possible infinite generator to block script execution.
    It is also passed as 'total' parameter to 'tqdm' progress bar.
    """
    results = thread_map(
        func, islice(sequence, max_sequence_length), total=max_sequence_length
    )
    return list(results)


def create_user(client: APIClient, kwargs: dict) -> User:
    assert "user_index" in kwargs

    username, password = generate_user_credentials(kwargs["user_index"])
    user = User(username=username, password=password, access_token=None, user_id=None)
    client.sign_up(user)
    client.authenticate(user)
    return user


def create_post(client: APIClient, kwargs: dict) -> int:
    assert "user" in kwargs

    content = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
        "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
        "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute "
        "irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
        "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia "
        "deserunt mollit anim id est laborum."
    )
    post = client.create_post(kwargs["user"], content)
    return post["id"]


def like_post(client: APIClient, kwargs: dict) -> int:
    assert "user" in kwargs and "post_id" in kwargs

    like = client.like_post(kwargs["user"], kwargs["post_id"])
    return like["id"]


def post_authors_generator(
    users: List[User], number_of_posts_for_each_user: List[int]
) -> Generator[Dict[str, Any], None, None]:
    """This generator yields a User (author) object for each Post that is
    about to be created. If more than one Post need to be created by a
    single User, this User's object will be yielded several times in a row.
    :param users: a list of users (authors).
    :param number_of_posts_for_each_user: a list of numbers where:
        - Number position (index) represents a User with the same index from 'users' list.
        - Number value represents a number of Posts that need to be created for this User.
    :return: {"user": Type[User]}
    """
    assert len(users) == len(number_of_posts_for_each_user)

    for i, user in enumerate(users):
        for _ in range(number_of_posts_for_each_user[i]):
            yield {"user": user}


def posts_to_like_generator(
    users: List[User], post_ids: List[int], number_of_likes_for_each_user: List[int]
) -> Generator[Dict[str, Any], None, None]:
    """This generator yields a User object and Post ID
    which is about to receive a Like from this User.
    :param users: a list of users.
    :param post_ids: a list of all available Posts IDs to randomly choose from.
    :param number_of_likes_for_each_user: a list of numbers where:
        - Number position (index) represents a User with the same index from 'users' list.
        - Number value represents a number of Posts that need to be liked by this User.
    :return: {"user": Type[User], "post_id": int}
    """
    assert len(users) == len(number_of_likes_for_each_user)

    for i, user in enumerate(users):
        post_ids_to_like = random.sample(post_ids, number_of_likes_for_each_user[i])
        for post_id in post_ids_to_like:
            yield {"user": user, "post_id": post_id}


def generate_user_credentials(index: int) -> Tuple[str, str]:
    # time_ns() is needed to avoid collisions on subsequent executions
    username = f"user_{index:04d}_{time.time_ns()}"
    password = f"password_{index:04d}"
    return username, password


def parse_arguments() -> Dict:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        required=False,
        default=DEFAULT_CONFIG_PATH,
        help=f'Path to configuration file (default: "./{os.path.basename(DEFAULT_CONFIG_PATH)}")',
    )
    parser.add_argument(
        "-u",
        "--url",
        required=False,
        default=DEFAULT_API_URL,
        help=f'API root URL (default: "{DEFAULT_API_URL}")',
    )
    return vars(parser.parse_args())


def parse_config(config_file_path: str) -> Dict[str, Any]:
    if not os.path.isfile(config_file_path):
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

    parser = ConfigParser()
    parser.read(config_file_path)

    settings = {}
    for key, value in parser.items(parser.default_section):
        expected_type = SETTINGS_FIELDS.get(key, str)
        try:
            value = expected_type(value)
        except ValueError as exc:
            raise ValueError(
                f'Invalid configuration: "{key}" expected to be of type {expected_type}'
            ) from exc

        settings[key] = value

    return settings


if __name__ == "__main__":
    main()
