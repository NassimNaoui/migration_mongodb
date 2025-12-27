from unittest.mock import patch, MagicMock
import app.sample.main as main_module

@patch('app.sample.main.dataLoader')
def test_main_data_loader(mock_loader):
    mock_loader.return_value.load_many_docs = MagicMock()
    main_module.main()
    mock_loader.return_value.load_many_docs.assert_called()
