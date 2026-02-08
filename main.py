import home_budget
from loguru import logger
from home_budget.config import CONFIG


def main():
    logger.info("Hello from home-budget!")
    logger.info(f"Configuration: {CONFIG.model_dump_json(indent=2)}")


if __name__ == "__main__":
    main()
