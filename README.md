# image_pyconverter_cli

---------------------------------------

[![PyPI version](https://badge.fury.io/py/image_pyconverter_cli.svg)](https://badge.fury.io/py/image_pyconverter_cli)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/image_pyconverter_cli)
![Github CI](https://github.com/shuntaH/image_pyconverter_cli/actions/workflows/test-ci.yml/badge.svg)

CLI providing simple image conversion functionality in python.

New features will be added as needed.


## Install
```bash
$ pip install image_pyconverter_cli
```

## Uninstall
```bash
$ pip uninstall image_pyconverter_cli
```



## Rename
A text file of the record before and after the conversion of the image is automatically created.

### 1
```bash
$ ic_rename directory-containing-images --is_all_replaced_with_new_name --new_name new-name
```
```bash
directry-containing-images
├── dir1
│   ├── dir1-image.png
│   └── dir2
│       └── dir2-image.png
└── image.png


directry-containing-imagesg-images
├── dir1
│   ├── new-name002.png
│   └── dir2
│       └── new-name003.png
└── new-name001.png
```

### 2
```bash
$ ic_rename directory-containing-images --chars_before_replacement dir1 dir2 --chars_after_replacement newdir1 newdir2
```
```bash
directry-containing-images
├── dir1
│   ├── dir1-image.png
│   └── dir2
│       └── dir2-image.png
└── image.png


directry-containing-images
├── dir1
│   ├── newdir1-image.png
│   └── dir2
│       └── newdir2-image.png
└── image.png
```

### 3
```bash
$ ic_rename directory-containing-images
```
```bash
directry-containing-images
├── dir1
│   └── ＡＢＣ.png
└── image００１.png


directry-containing-images
├── dir1
│   └── abc.png
└── image001.png
```


### 4
```bash
$ ic_rename directory-containing-images --is_separator_and_delimiter_replaced --separator _
```
```bash
directry-containing-images
├── dir1
│   ├── dir1-image.png
│   └── dir2
│       └── dir2-image.png
└── image image.png


directry-containing-images
├── dir1
│   ├── dir1_image.png
│   └── dir2
│       └── dir2_image.png
└── image_image.png
```

### 5
```bash
$ ic_rename directory-containing-images --alternative_unavailable_char_in_windows -
```
```bash
directry-containing-images
└── -_,!(:*?<>|¥)あabc.png


directry-containing-images
└── -_,!(--------)あabc.png
```

### 6
```bash
$ ic_rename directory-containing-images --alternative_url_encoded_char X
```
```bash
directry-containing-images
└── -_,!()abcあ* &^%.png


directry-containing-images
└── -_XXXXabcXXXXXX.png
```

### 7
```bash
$ ic_rename directory-containing-images --prefix prefix --suffix suffix --separator -
```
```bash
directry-containing-images
└── image.png


directry-containing-images
└── prefix-image-suffix.png
```

### 8
```bash
$ ic_rename directory-containing-images --prefix prefix --suffix suffix --separator -
```
```bash
directry-containing-images
└── image.png


directry-containing-images
└── prefix-image-suffix.png
```

### 9
```bash
$ ic_rename directory-containing-images --is_serial_number_added
```
```bash
directry-containing-images
├── dir1
│   ├── dir1-image.png
│   └── dir2
│       └── dir2-image.png
└── image.png


directry-containing-images
├── dir1
│   ├── dir1-image002.png
│   └── dir2
│       └── dir2-image003.png
└── image001.png
```


### 10
```bash
$ ic_rename directory-containing-images --is_output_to_same_dir --separator -
```
```bash
directry-containing-images
├── dir1
│   ├── image.png
│   └── dir2
│       └── image.png
└── image.png


directry-containing-images
├── dir1-image.png
├── dir2-image.png
└── image.png
```
