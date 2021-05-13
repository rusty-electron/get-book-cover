# get-book-cover
a simple python script to download book covers from the api of openlibrary.org

### usage 

```python
python main.py -q "<book-name>" -d "<output-dir>"

# output-dir is optional
```
* script will get an image and show it to you
* it will then wait for input
    * press `y` to save it, it will ask you for the filename (do add extension)
    * press `n` to skip and show next image
    * press `q` to quit

images are saved by default to `./img`

### info

* check api docs [here](https://openlibrary.org/developers/api).
