from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from database.database import Base
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


config.set_section_option("alembic", "DB_USER", os.getenv("DB_USER"))
config.set_section_option("alembic", "DB_PASSWORD", os.getenv("DB_PASSWORD"))
config.set_section_option("alembic", "DB_DATABASE", os.getenv("DB_DATABASE"))
config.set_section_option("alembic", "DB_HOST", os.getenv("DB_HOST"))
config.set_section_option("alembic", "DB_PORT", os.getenv("DB_PORT"))


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from models.access_token import AccessToken
from models.answers import Answers
from models.companies import Companies
from models.company_billing_info import CompanyBillingInfo
from models.company_billing_statuses import CompanyBillingStatuses
from models.company_receipts import CompanyReceipts
from models.company_transaction_histories import CompanyTransactionHistories
from models.course_progresses import CourseProgresses
from models.courses import Courses
from models.curriculum_progresses import CurriculumProgresses
from models.curriculums import Curriculums
from models.devices import Devices
from models.learning_records import LearningRecords
from models.learning_statuses import LearningStatuses
from models.mentorships import Mentorships
from models.news import News
from models.payment_methods import PaymentMethods
from models.questions import Questions
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses
from models.roles import Roles
from models.section_progresses import SectionProgresses
from models.section_tags import SectionTags
from models.sections import Sections
from models.tags import Tags
from models.test_contents import TestContents
from models.user_account_info import UserAccountInfo
from models.user_account_types import UserAccountTypes
from models.user_reward_histories import UserRewardHistories
from models.user_rewards import UserRewards
from models.users import Users
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
