# Braingeneers Mission Control

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- ABOUT THE PROJECT -->
## About The Project
This repository contains the source code and related resources for the Braingeneers Mission Control project. Braingeneers Mission Control is a baseline for developing Docker containers including the `braingeneerspy` package on the [National Research Platform (NRP)](https://nationalresearchplatform.org).

### Built With

* [![Docker][docker-shield]][docker-url]
* [![Unix-shell][shell-shield]][shell-url]
* [![Python][python-shield]][python-url]

<!-- GETTING STARTED -->
## Getting Started
These instructions will guide you on how to get started with the Braingeneers Mission Control repository. By following these steps, you'll be able to set up the necessary dependencies and run the code locally.

### Prerequisites
To use the Braingeneers Mission Control repository, you'll need the following prerequisites:

1. Docker: Make sure you have Docker installed on your machine. You can download Docker from the official website: https://www.docker.com/get-started
2. Git: You'll need Git installed to clone the repository. You can download Git from the official website: https://git-scm.com/downloads

<!-- USAGE EXAMPLES -->
## Usage
Follow these steps to set up and use the Braingeneers Mission Control repository:

1. Clone the repository:
```
git clone https://github.com/braingeneers/mission-control.git
```

2. Change into the cloned directory:
```
cd mission-control
```

3. Build the Docker image:
```
docker build -t braingeneers-mission-control .
```

4. Run the Docker container:
```
docker run -it braingeneers-mission-control
```

This command will start the Docker container and launch the Braingeneers Mission Control application.
5. Access the Mission Control application:
Once the container is running, you can access the Mission Control application by opening a web browser and navigating to http://localhost:8888.
You will be prompted to enter a token for authentication. Look for the token in the terminal output where you started the Docker container. It will be displayed in a log line similar to:
```
To access the notebook, open this file in a browser:
    file:///home/jovyan/.local/share/jupyter/runtime/nbserver-6-open.html
Or copy and paste one of these URLs:
    http://(container-id or 127.0.0.1):8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

6. Copy the complete URL with the token and paste it into your browser. This will open the Braingeneers Mission Control notebook interface.
Explore the Mission Control notebook:
Once you're in the notebook interface, you can explore the available notebooks and interact with the Braingeneers Mission Control functionality. Follow the instructions provided within the notebooks to perform various tasks and analyses.

That's it! You're now ready to use the Braingeneers Mission Control repository and explore the capabilities it offers. Feel free to modify the code, experiment with different parameters, and contribute to the project as you see fit.

Please note that the above instructions assume a basic understanding of Docker and Git. If you're unfamiliar with these tools, you may want to refer to their respective documentation to learn more about their usage and concepts.

I hope this helps! Let me know if you have any further questions.

<!-- ROADMAP -->
## Roadmap

- [ ] Update README.md
- [ ] Setup CI/CD Pipeline
- [ ] Build Braingeneers Docker image
- [ ] Add Docker image to ghcr.io
- [ ] Connect Braingeneers Docker image to `wetai-docker` repo

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/new_feature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/new_feature`)
5. Open a Pull Request

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/uw-ssec/wetai-mc?style=for-the-badge
[contributors-url]: https://github.com/uw-ssec/wetai-mc/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/uw-ssec/wetai-mc?style=for-the-badge
[forks-url]: https://github.com/uw-ssec/wetai-mc/network/members
[stars-shield]: https://img.shields.io/github/stars/uw-ssec/wetai-mc?style=for-the-badge
[stars-url]: https://github.com/uw-ssec/wetai-mc/stargazers
[issues-shield]: https://img.shields.io/github/issues/uw-ssec/wetai-mc?style=for-the-badge
[issues-url]: https://github.com/uw-ssec/wetai-mc/issues

[docker-shield]: https://img.shields.io/badge/Docker-0db7ed?style=for-the-badge&logo=docker&logoColor=white
[docker-url]: https://www.docker.com/
[shell-shield]: https://img.shields.io/badge/Shell-4eaa25?style=for-the-badge&logo=gnubash&logoColor=white
[shell-url]: https://www.opengroup.org
[python-shield]: https://img.shields.io/badge/Python-646464?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org
