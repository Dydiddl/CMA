from setuptools import setup, find_packages

setup(
    name="backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "pydantic",
        "pydantic-settings",
        "python-dotenv",
        "email-validator",
        "python-docx",
        "openpyxl",
        "xlsxwriter",
        "aiofiles",
        "python-dateutil",
        "pytest",
        "pytest-asyncio",
        "pytest-cov"
    ],
) 