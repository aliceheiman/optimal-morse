<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<div align="center">

<h3 align="center">Optimal Morse</h3>

  <p align="center">
    An exploration into the optimal morse code for English and Swedish based on their respective letter frequencies.
    <br />
    <a href="#">View Demo</a>
    ·
    <a href="https://github.com/aliceheiman/optimal-morse/issues">Report Bug</a>
    ·
    <a href="https://github.com/aliceheiman/optimal-morse/issues">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

The Morse Code maps each letter to a sequence of dots and dashes.

How do you determine which sequence each letter should receive? If you think about it, you would probably want the most common letters to have shorter sequences, and the letters that are not used that much to get the longer sequences.

I performed a letter frequency analysis using the Python NLTK library, the NLTK Brown corpus, and Språkbankens Swedish corpus 'talbanken' together with their python module 'sb-nltk-tools'. Check out my results in the demo!

[You can find the application here]()

### Built With

* Python
* Streamlit

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/aliceheiman/optimal-morse.git
   ```
2. Install pip packages
   ```sh
   ppip install -r requirements.txt
   ```
3. Run streamlit
   ```sh
   streamlit run app.py
   
And that's it! 👏

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

<!-- CONTACT -->
## Contact

Alice Heiman - aheiman@stanford.com

Project Link: [https://github.com/aliceheiman/optimal-morse](https://github.com/aliceheiman/optimal-morse)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/aliceheiman/optimal-morse.svg?style=for-the-badge
[contributors-url]: https://github.com/aliceheiman/optimal-morse/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/aliceheiman/optimal-morse.svg?style=for-the-badge
[forks-url]: https://github.com/aliceheiman/optimal-morse/network/members
[stars-shield]: https://img.shields.io/github/stars/aliceheiman/optimal-morse.svg?style=for-the-badge
[stars-url]: https://github.com/aliceheiman/optimal-morse/stargazers
[issues-shield]: https://img.shields.io/github/issues/aliceheiman/optimal-morse.svg?style=for-the-badge
[issues-url]: https://github.com/aliceheiman/optimal-morse/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/alice-heiman-311105213/
[font-image]: assets/front-page.png
[practice-image]: assets/practice.png
