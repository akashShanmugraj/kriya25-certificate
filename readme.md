# README for Certificate Generation API

## Overview

The `generate_certificate` endpoint is a Flask API that dynamically generates a personalized certificate PDF based on the provided user data. The endpoint accepts a JSON payload containing the student's details, merges the text into a certificate template, and returns the generated certificate as a downloadable file.

## Endpoint Details

### URL

```
POST /generate_certificate
```

### Request Payload

The endpoint accepts a JSON payload with the following fields:

| Field     | Type   | Required | Default Value    | Description                                       |
| --------- | ------ | -------- | ---------------- | ------------------------------------------------- |
| `name`    | string | Yes      | N/A              | Name of the student to appear on the certificate. |
| `college` | string | Yes      | N/A              | Name of the college to appear on the certificate. |
| `course`  | string | No       | `General Course` | Name of the course to appear on the certificate.  |
| `date`    | string | No       | `13 - 12 - 2024` | Date to appear on the certificate.                |

Example request body:

```json
{
  "name": "John Doe",
  "college": "XYZ University",
  "course": "Computer Science",
  "date": "01 - 01 - 2024"
}
```

### Response

#### Success Response

If the certificate is successfully generated, the API returns a downloadable file:

- **Status Code:** `200 OK`
- **Content:** The generated PDF file as an attachment.

#### Error Responses

The API handles errors gracefully and returns appropriate error messages:

1. **Missing Required Fields:**

   - **Status Code:** `400 Bad Request`
   - **Response:**
     ```json
     {
       "error": "Name and college are required fields"
     }
     ```

2. **Error While Drawing Text:**

   - **Status Code:** `500 Internal Server Error`
   - **Response:**
     ```json
     {
       "error": "Error while drawing text on canvas: [Error Details]"
     }
     ```

3. **Error While Merging or Saving PDF:**

   - **Status Code:** `500 Internal Server Error`
   - **Response:**
     ```json
     {
       "error": "Error while merging or saving the PDF: [Error Details]"
     }
     ```

4. **Error While Sending the File:**

   - **Status Code:** `500 Internal Server Error`
   - **Response:**
     ```json
     {
       "error": "Error while sending the file: [Error Details]"
     }
     ```

5. **Unexpected Error:**
   - **Status Code:** `500 Internal Server Error`
   - **Response:**
     ```json
     {
       "error": "An unexpected error occurred",
       "details": "[Error Details]"
     }
     ```

### Example Usage

#### cURL Command

```bash
curl -X POST http://<host>:<port>/generate_certificate \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "college": "XYZ University",
  "course": "Computer Science",
  "date": "01 - 01 - 2024"
}' --output John_Doe_certificate.pdf
```

### Notes

- Ensure the `Input/certificate_template.pdf` file exists and is correctly formatted.
- Fonts (`VeraBd.ttf`, `Vera.ttf`, `VeraBI.ttf`) must be available in the appropriate directory.
- Generated certificates are stored temporarily in the `Certificates` folder.
- Customize default values (`course`, `date`) as needed.

### Environment Setup

To run the API, ensure you have the following dependencies installed:

- Python 3.7+
- Flask
- reportlab
- PyPDF2

#### Install Dependencies

```bash
pip install flask reportlab PyPDF2
```

#### Run the Application

```bash
python <filename>.py
```

The application will be available at `http://127.0.0.1:5000` by default.
