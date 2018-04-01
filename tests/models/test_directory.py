from unittest.mock import patch, MagicMock, Mock, call
import pytest
from app.models import directory


def test_directory():
    dir = directory.Directory('/home')
    assert len(dir.contents) != 0


# for debugging
if __name__ == '__main__':
    pytest.main()
