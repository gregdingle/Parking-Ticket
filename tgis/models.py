#from django.db import models
from django.contrib.gis.db import models
# Create your models here.

class Location(models.Model):
	name = models.CharField(max_length=255)
	point = models.PointField(help_text='Represented as (lan, lat)')
	objects = models.GeoManager()

class Region(models.Model):
	name = models.CharField(max_length=255)
	area = models.PolygonField()
	objects = models.GeoManager()

class Paths(models.Model):
	path = models.LineStringField(srid=4269)
	badge = models.CharField(max_length=255)
	day = models.DateField()
	chunk = models.IntegerField()
	start_address = models.CharField(max_length=255)
	end_address = models.CharField(max_length=255)
	start_datetime = models.DateTimeField()
	end_datetime = models.DateTimeField()
	waypoints = models.MultiPointField(srid=4269)
	objects = models.GeoManager()

	class Meta:
		db_table = "paths"

class Tickets(models.Model):
	ag = models.IntegerField()
	citation = models.CharField(max_length=255)
	issue_datetime = models.DateTimeField()
	plate = models.CharField(max_length=255)
	vin = models.CharField(max_length=255)
	make = models.CharField(max_length=255)
	body = models.CharField(max_length=255)
	cl = models.CharField(max_length=255)
	location = models.CharField(max_length=255)
	badge = models.CharField(max_length=255)
	violation = models.CharField(max_length=255)
	violation_description = models.TextField(max_length=255)
	meter = models.CharField(max_length=255)
	fine_amt = models.DecimalField(max_digits=4,decimal_places=2)
	penalty_1 = models.DecimalField(max_digits=4,decimal_places=2)
	penalty_2 = models.DecimalField(max_digits=4,decimal_places=2)
	penalty_4 = models.DecimalField(max_digits=4,decimal_places=2)
	penalty_5 = models.DecimalField(max_digits=4,decimal_places=2)
	pay_amt = models.DecimalField(max_digits=4,decimal_places=2)
	outstanding = models.DecimalField(max_digits=4,decimal_places=2)
	s = models.CharField(max_length=255)
	geopoint = models.PointField(srid=4269)

	objects = models.GeoManager()

	class Meta:
		db_table = "tickets"
