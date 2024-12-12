import logging
import sys
import inspect
from app.challenge.challenge_goal import ChallengeGoal
from app.astral_objects.polyanet import Polyanet
from app.astral_objects.soloon import Soloon
from app.astral_objects.cometh import Cometh

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def main():
#     try:
#         # Initialize the ChallengeGoal class
#         challenge = ChallengeGoal()
#         print()

#         # Retrieve the goal map
#         logger.info("Retrieving the goal map...")
#         challenge.get_goal_map()

#         # Solve the challenge
#         logger.info("Solving Challenge 1...")
#         challenge.solve_challengue_1()

#         logger.info("Challenge 1 solved successfully!")
#     except Exception as e:
#         logger.error(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_supported_challenges():
    """Dynamically detect all solve_challengue_X methods in ChallengeGoal."""
    methods = inspect.getmembers(ChallengeGoal, predicate=inspect.isfunction)
    challenge_methods = {
        int(name.split("_")[-1]): name
        for name, _ in methods
        if name.startswith("solve_challengue_") and name.split("_")[-1].isdigit()
    }
    return challenge_methods


def main():
    # Ensure the program receives a challenge number as input
    if len(sys.argv) != 2:
        print("Usage: python main.py <challenge_number>")
        print("Example: python main.py 1")
        sys.exit(1)

    # Parse the challenge number from the command line
    try:
        challenge_number = int(sys.argv[1])
    except ValueError:
        print("Challenge number must be an integer (e.g., 1 or 2).")
        sys.exit(1)

    # Dynamically detect supported challenges
    supported_challenges = get_supported_challenges()

    if challenge_number not in supported_challenges:
        print(f"Challenge {challenge_number} is not supported.")
        print(f"Supported challenges are: {sorted(supported_challenges.keys())}")
        sys.exit(1)

    # Initialize the ChallengeGoal class
    challenge = ChallengeGoal()

    # Call the appropriate method based on the challenge number
    try:
        logger.info(f"Starting Challenge {challenge_number}...")
        challenge.get_goal_map()
        method_name = supported_challenges[challenge_number]
        getattr(challenge, method_name)()
        logger.info(f"Challenge {challenge_number} completed successfully!")
    except Exception as e:
        logger.error(
            f"An error occurred while solving Challenge {challenge_number}: {e}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
