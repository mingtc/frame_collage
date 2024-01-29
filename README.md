<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">


  <h3 align="center">Frame Collage</h3>

  <p align="center">
    A set of layout containers and scripts for generating collages via batch processing.
    <br />
  </p>
</div>





<!-- ABOUT THE PROJECT -->
## About The Project

This project started as a desire to generate images for the Samsung Frame TV where the official app has performance issues and has feature limitations.
As well, other apps may require more complex setups that might not fit the purpose and/or can cost money.
The priority of this project are abstraction, extensibility, and performance.

This is achieved by:
Abtraction: All layout containers implements a common abstract class and layout algorithms can call class methods without knowing which class instance each container is.
As well, the layout container itself can call on child layout and items without knowing their class.

Extensibility: With the abstraction, adding more layout types or layout item types will be simple. Common code is extracted to the abstract class but still can be overriden if there is a need.
As well, containers themselves deal with abstract containers and objects, as long as it has a 2d dimension, the containers will work with it.  This can lend itself to other applications.

Performance: Image handling uses CV2 and Numpy. Aside from taking advantage of vectorization, the actual image manipulation does not happen until the final output leaving resizing / movements lightweight.


The current version includes only the containers and scripts for generating collages. Here is a rough plan for this project:
* Create basic building blocks such as containers and container item objects
* Create scripts that uses these building blocks to generate output
* Create a GUI that gets the files + configurations for running the script from the user
* Offer stylized image filters, image frames, and exif data reading
* Create or adapt more advanced layout algorithms 
* Generalize as all-purpose collage creation app


<!-- GETTING STARTED -->
## Getting Started

Run main.py after modifying the input and output directories in the code. 
Examine layout_generator.py for more details on tweaking.
Current version is not ready for general use.


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

This readme template is based from https://github.com/othneildrew/Best-README-Template 








