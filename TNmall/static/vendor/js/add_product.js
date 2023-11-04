const imageContainer = document.querySelector('.image-container');
      const uploadIcon = imageContainer.querySelector('.upload-icon');
      const previewImage = imageContainer.querySelector('#preview-image');
      const inputImage = imageContainer.querySelector('#input-image');

      uploadIcon.addEventListener('click', () => {
        inputImage.click();
      });

      inputImage.addEventListener('change', () => {
        const file = inputImage.files[0];
        if (file) {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => {
            previewImage.src = reader.result;
            previewImage.style.display = 'block';
            uploadIcon.style.display = 'none';
          }
        }
      });