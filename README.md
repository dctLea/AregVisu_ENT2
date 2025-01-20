** AregTec - Canine Anatomy Module

**Overview
This repository houses the Drupal module responsible for creating a digital interactive canine anatomy model as part of the AregTec project. The AregTec initiative aims to develop a comprehensive electronic medical record for veterinary professionals.
This specific module focuses on:
Visual representation: A detailed skeletal structure of a dog is rendered.
User interaction: Veterinary professionals can interact with the model, selecting specific bones or regions for further examination.
Purpose This module is designed to provide a visually engaging and interactive tool for veterinary students and practitioners to enhance their understanding of canine anatomy. It serves as a foundational component for the larger AregTec project.

**Installation and Usage**

  **Prerequisites:**
The Drupal site is containerized using Docker, sharing the infrastructure with a MySQL container for the AregTec project database. To run this module, you'll need to get the docker-compose.yml file and customize it to fit your local setup and the directory structure of this Git repository.
Currently, the Drupal page is not working. To display Python scripts, we recommend using a software application that can execute Python scripts.
 
  **Installation:**
The folder present in the Git should be downloaded and install in the “module” folder of the “Drupal” folder, created when the docker-compose.yml has been executed. 
The database is empty, so you will have to fill it with the coordinates given. 
In the “Images” folder, you will find the images of the bones that are used for the visualization of the skeleton. 
