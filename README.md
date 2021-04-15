<<<<<<< HEAD
# Repo for the project: p-0920-eth-lab

all non-coding related documents are available on a [shared google drive folder](https://drive.google.com/drive/folders/10yA8OL2weX9hFvfQLHT_0aeY4aa-iYp3?usp=sharing)


## Work plan (updated 26.10)
### Preprocessing:
#### Getting the outline of plants
	Libraries to try. https://opensource.com/article/19/3/python-image-manipulation-tools

#### ?? Get the structure of specimen (in order to localize better flowers and fruits)
- Interpolate pixels under the tape  
- Translate outline into simple vector/graph structures OR


#### Localise “hot” areas for flower and fruits
e.g following https://github.com/matterport/Mask_RCNN & https://www.frontiersin.org/articles/10.3389/fpls.2020.01129/full

### Labelling training data:    
Possibilities:
- Manual labelling of 200-300 pictures   
- Active learning ??   
- One shot learning?   
- Use date and location as fuzzy classifier?   
Define Class balance / species balance    
E.g. Number of flowers, Number of stems with fruits    

### Classification:
 From project description
> Obviously, you should score a herbarium sheet (i) as flowering, when you can ‘clearly’ distinguish flowers, (ii) as fruiting, when you can ‘clearly’ distinguish fruits (siliques or silicles, depending on the species), (iii) as both flowering and fruiting, when you can ‘clearly’ distinguish flowers and fruits on a given voucher (see ZT-00142092 or ZT-00142096 as an example), and (iv) at the vegetative stage, when you cannot distinguish either flowers or fruits on a given voucher, but solely leaves and stems. Caution, there is a time-point, right after pollination, when flowers have just wilted, but fruits have already started to develop; under such circumstances, petals may still be apparent, but fruits may already protrude out of the flowers. I suggest to score such specimens as ‘ambiguous’, because neither flowers, nor fruits can be ‘clearly’ distinguished (see specimen ZT-00081542 as an example).

#### Multilabel classification with 3 categories:   
- Flowering: flowers present on the top on the stems   
- Fruit: fruit pods / Elongated or round pods along the main stem   
- Both fruits and flower: dixit  
- None: vegetative state (possibly under-represented category),  
- Ambiguous: in transition between flowers and fruits   

### Interpretation:  
- Map with location and phenology info? 


## Files and explanation

helper_function.py : custom function that are useful across all notebooks.  
requirements.txt : list of required packages and libraries `pip freeze > requirements.txt`  
001_data_loading.ipynb : how to access the data in the google bucket   
002_outline detction: dixit

## Log

=======
## Daily Outline

### October 26
- Started reviewing provided data and goals of the project
- Created questions for meeting with Barry and Dr. Guggisberg tomorrow
- Background research on other herbarium classification tasks
- discussed possible shortcomings of images and technology

TODO 
- decide how we want to label the photos
- make plan of action which models to try first

### October 27
Meeting with Barry
decide daily workflow and project goals after

Post meeting TODO:
- Google cloud free service
- Run trial models with public labeled dataset from paper
- Label photos 
- Export labels in COCO format
- Add overall classification to image metadata
- create bounding box workflow and ensure it works with full res images


>>>>>>> f206237e4f063ca425bb584ef5199ec3d84edb05
