**Author:** Behrouz Safari
**Website:** [AstroDataScience.Net](http://astrodatascience.net/)<br/>

# distars
*Analysing distance of stars*

## count

To count number of object in a circle use the function *count*; pass the center of circle with a radius and specify a database.

```python
>>> from distars.regions import count
>>> ra, dec = 309.3918000320833, -47.2915007225
>>> radius = 1 # degree
>>> n = count(ra, dec, radius, database='simbad')
>>> print(n)
1067
```

You can pass to *where* argument a condition. Let's use Gaia data realese 3 this time:

```python
>>> n = count(ra, dec, radius, database='gaia', where='radial_velocity IS NOT NULL')
>>> print(n)
1413
```