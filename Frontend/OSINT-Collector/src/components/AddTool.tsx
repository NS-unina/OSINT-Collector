import React, { useState, useRef } from "react";
import axios from "axios";
import AlertMessage from "./AlertMessage";

const AddTool = () => {
  const [selectedFileName, setSelectedFileName] = useState<string>("");
  const [fileInput, setFileInput] = useState<FileList | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState<boolean | null>(null);

  const dragDropAreaRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    dragDropAreaRef.current?.classList.add("border-primary", "rounded");
  };

  const handleDragLeave = () => {
    dragDropAreaRef.current?.classList.remove("border-primary", "rounded");
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    dragDropAreaRef.current?.classList.remove("border-primary", "rounded");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      setFileInput(files);
      updateFileName(files[0]);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      setFileInput(files);
      updateFileName(files[0]);
    }
  };

  const handleDragDropAreaClick = () => {
    fileInputRef.current?.click();
  };

  const updateFileName = (file: File) => {
    setSelectedFileName(file ? `Selected File: ${file.name}` : "");
  };

  const handleFormSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!fileInput || fileInput.length === 0) {
      // Non ci sono file selezionati
      return;
    }

    const formData = new FormData();
    formData.append("yaml_file", fileInput[0]);

    axios
      .post("http://localhost:8080/tools/add", formData)
      .then(() => {
        console.log("Upload completato con successo!");
        setUploadSuccess(true);
      })
      .catch((error) => {
        console.error("Errore durante la richiesta al server:", error);
        setUploadSuccess(false);
      })
      .finally(() => {
        setFileInput(null);
        setSelectedFileName("");
      });
  };

  return (
    <div className="container mt-5">
      <form
        method="post"
        encType="multipart/form-data"
        className="mb-4"
        id="add-tool-form"
        onSubmit={handleFormSubmit}
      >
        <div
          className="drag-drop-area border rounded p-5"
          id="drag-drop-area"
          ref={dragDropAreaRef}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleDragDropAreaClick}
        >
          <p className="mb-0">
            Drag & drop a YAML file here or click to select one.
          </p>
          <input
            type="file"
            className="form-control-file d-none"
            id="yaml_file"
            name="yaml_file"
            accept=".yaml, .yml"
            onChange={handleFileInputChange}
            multiple={false}
            ref={fileInputRef}
          />
          <div id="file-name" className="mt-2">
            {selectedFileName}
          </div>
        </div>
        <button
          type="submit"
          className={`btn btn-success mt-3 ${!fileInput ? "btn-disabled" : ""}`}
          disabled={!fileInput || fileInput.length === 0}
        >
          Add
        </button>
      </form>
      {uploadSuccess !== null && (
        <AlertMessage
          message={
            uploadSuccess
              ? "Upload completed successfully!"
              : "Error uploading file."
          }
          type={uploadSuccess ? "success" : "danger"}
          onClose={() => setUploadSuccess(null)}
        />
      )}
    </div>
  );
};

export default AddTool;
