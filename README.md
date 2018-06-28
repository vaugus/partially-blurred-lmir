## Partially Blurred Light Microscopy Image Restoration - partially-blurred-lmir
### Digital Image Processing - ICMC - 2018
Victor Augusto Alves Catanante - 10839918

- How to run (Linux):

  $ chmod +x execute.sh
  
  $ ./execute.sh <method>

  methods:
    - 1: inverse filtering
    - 2: wiener filtering with gamma parameter
    - 3: wiener filter with spectrum approach
    - 4: wiener filter, as proposed by scikit-learn package
    - 5: richardson-lucy, as proposed by scikit-learn package
    - 6: laplacian kernel convolution 
