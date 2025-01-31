# AregTec - Canine Anatomy Module

## Overview
This repository houses the **Drupal module** responsible for creating a **digital interactive canine anatomy model** as part of the **AregTec** project.  
The AregTec initiative aims to develop a **comprehensive electronic medical record** for veterinary professionals.

### This specific module focuses on:
- **Visual representation**: A detailed skeletal structure of a dog is rendered.
- **User interaction**: Veterinary professionals can interact with the model, selecting specific bones or regions for further examination.

## Purpose
This module is designed to provide a **visually engaging** and **interactive** tool for veterinary students and practitioners to enhance their understanding of **canine anatomy**.  
It serves as a **foundational component** for the larger **AregTec** project.

---

## Introduction

### Explanation of Important Folders and Files

- **FOLDER** `images_resized` : Folder containing the resized bone images used.
- **FOLDER** `volumes/modules/custom` : Contains the custom **Drupal module** to run the code.
- **FILE** `Peuplement_BDD_graph.sql` : **SQL script** for populating the database.
- **FILE** `Nodes_graph.py` : Constructs the **graph of points** at the respective coordinates of the bones.
- **FILE** `Dashboard_graph.py` :  
  - Python code returning a **Tkinter interface** with the **interactive graph** (zoom in/out/move).  
  - **Text search mode** *(not implemented)*.  
  - **Voice search mode** *(not implemented)*.  
- **FILE** `Graphe_Simple.py` : Python code displaying only the **interactive graph** (zoom in/out/move).
- **FILE** `docker-compose.yml` : Configuration file for setting up the **Docker environment**.

---

## Installation and Usage

### Prerequisites
The **Drupal site** is containerized using **Docker**, sharing the infrastructure with a **MySQL container** for the AregTec project database.  
To run this module, you will need to get the **docker-compose.yml** file and customize it to fit your local setup and the directory structure of this Git repository.

> ⚠ **Currently, the Drupal page is not working.**  
> To display **Python scripts**, we recommend using a software application that can execute Python scripts.

### Installation
1. Download the **folder present in the Git repository**.  
2. Place it inside the **"module" folder** of the **"Drupal" folder**, created when the **docker-compose.yml** is executed.  
3. The database is **empty**, so you will need to populate it with the given script: `Peuplement_BDD_graph.sql`.
