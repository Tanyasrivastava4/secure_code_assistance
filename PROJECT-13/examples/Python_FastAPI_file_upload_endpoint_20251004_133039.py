Python FastAPI file upload endpoint

### Installation

```bash
pip install fastapi-file-upload
```

### Usage

```python
from fastapi import FastAPI
from fastapi_file_upload import FileUpload

app = FastAPI()

file_upload = FileUpload()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return await file_upload.save(file)
```

### Configuration

```python
file_upload = FileUpload(
    upload_dir="uploads",
    max_file_size=1024 * 1024 * 10,
    allowed_extensions=["jpg", "png", "jpeg"],
    allowed_content_types=["image/jpeg", "image/png"],
    allowed_content_transfer_encodings=["base64"],
)
```

### Parameters

- `upload_dir` - Directory where files will be saved. Default: `uploads`
- `max_file_size` - Maximum file size in bytes. Default: `1024 * 1024 * 10`
- `allowed_extensions` - List of allowed file extensions. Default: `[]`
- `allowed_content_types` - List of allowed content types. Default: `[]`
- `allowed_content_transfer_encodings` - List of allowed content transfer encodings. Default: `[]`

### Return

```python
{
    "filename": "test.jpg",
    "filepath": "uploads/test.jpg",
    "file_size": 1024,
    "content_type": "image/jpeg",
    "content_transfer_encoding": "base64",
    "extension": "jpg",
    "mimetype": "image/jpeg",
    "md5": "9f86d081884c7d659a2feaa0c55ad015",
    "sha1": "a678bfe266e4c1e58f262d3b20f7b0e77bbc42e4",
    "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    "sha512": "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f",
    "sha3_224": "348c890790a3f02583288b2e00e2ed0e613e9e3f312e1f40504e1883953953b",
    "sha3_256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    "sha3_384": "65587990219f40e254703f69f98060412009e8886d668748528155167563d9a4",
    "sha3_512": "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d