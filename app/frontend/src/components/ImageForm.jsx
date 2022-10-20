import React, {useState} from 'react'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import '../../node_modules/bootstrap/dist/css/bootstrap.css';

export const ImageForm = () => {
    const [selectedImage, setSelectedImage] = useState("")

    function onFileChange(e) {
        let files = e.target.files;
        let fileReader = new FileReader();
        fileReader.readAsDataURL(files[0]);

        fileReader.onload = (event) => {
            setSelectedImage(event.target.result.replace("data:", "").replace(/^.+,/, ""))
        }
    }

    function onSubmit() {
        console.log(selectedImage)
        let imageElement = document.getElementById('imageContainer')
        let endpoint = "http://0.0.0.0:5000/api/v1/process_image/";
        let data = {raw_image_base64: selectedImage}

        fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify(data),
        })
            .then(response => {
                return response

            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                imageElement.src = "data:image/jpg;base64," + data
            })
            .catch(error => {
                console.error(error);
            });
    }

    return (
        <div>
            <h1>Select file</h1>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                <img className="imageContainer" id="imageContainer" src=""/>
                <br/>
                <Form.Control formMethod="POST" formEncType="multipart/form-data" className="mb-3" type="file"
                              name="image" accept="image/jpeg, image/png, image/jpg" onChange={onFileChange}/>
                <br/>
                <Button variant="light" type="submit" onClick={() => onSubmit()}>
                    Upload
                </Button>
            </Form.Group>
        </div>

    )
}
