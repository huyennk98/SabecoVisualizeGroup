import json
import gzip
import zipfile
from io import BytesIO


def read_json_from_archive(input_file, decoded_file):
    if input_file.endswith('.zip'):
        with zipfile.ZipFile(BytesIO(decoded_file)) as z:
            # Assuming there is only one JSON file in the zip
            json_file_name = [f for f in z.namelist() if f.endswith('.json')][0]
            with z.open(json_file_name) as json_file:
                return json.loads(json_file.read().decode('utf-8'))

    elif input_file.endswith('.gzip') or input_file.endswith('.gz'):
        with gzip.open(BytesIO(decoded_file), 'rt', encoding='utf-8') as json_file:
            return json.load(json_file)

    elif input_file.endswith('.json'):
        return json.loads(decoded_file.decode('utf-8'))

    else:
        raise ValueError("Unsupported file format")
