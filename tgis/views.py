from django.template import loader, Context, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

from tgis.forms import addressForm
from django.db.models import *
from tgis.models import Paths, Tickets
from django.contrib.gis.geos import fromstr

def home(request):
	adForm = addressForm()
	
	if request.method == 'POST':
		if 'chance_of_ticket' in request.POST:
				address = request.POST['address']
				if address:
						longlat = getPoint(address)
						pnt = fromstr('POINT( %f %f)' % longlat,srid=4269)
				else:
						pnt = fromstr('POINT(-122.398595809937 37.7840061485767)', srid=4269)
				
				ticket_frequency = getTicketFrequency(pnt)
				return render_to_response('home.html',{'TF': ticket_frequency,'form': adForm}, context_instance=RequestContext(request))
		elif 'tell_me_the_laws' in request.POST:
				address = request.POST['address']
				if address:
						getlaws = getLaw(address)
				else:
						getlaws = getLaw('1045 PINE ST, San Francisco, CA')
				return render_to_response('home.html',{'form': adForm, 'PL': getlaws}, context_instance=RequestContext(request))

	else:
		return render_to_response('home.html',{'form': adForm,}, context_instance=RequestContext(request))
	

def getPoint(address):
		from geocode.google import GoogleGeocoderClient
		geocoder = GoogleGeocoderClient(False)
		result = geocoder.geocode(address)
		if result.is_success():
				longlat = result.get_location()
				lat = float(str(longlat[1]))
				lang = float(str(longlat[0]))
				return lat,lang


def getTicketFrequency(location=None, start_time=None, end_time=None):
	from time import mktime
	from datetime import datetime
	#pnt = fromstr('POINT(-122.398595809937 37.7840061485767)', srid=4269)
	if not location:
		P1 = Paths.objects.filter(path__dwithin=(pnt, 0.0001)).aggregate(end_datetime=Max('end_datetime'), start_datetime=Min('start_datetime'), cnt=Count('id'))

	else:
		pnt = location
		P1 = Paths.objects.filter(path__dwithin=(pnt, 0.0001)).aggregate(end_datetime=Max('end_datetime'), start_datetime=Min('start_datetime'), cnt=Count('id'))
	
	hours = (mktime(datetime.utctimetuple(P1['end_datetime'])) - mktime(datetime.utctimetuple(P1['start_datetime']))) / 366
	
	tickets_per_hour = (P1['cnt'] / hours) * 100
	P1['hours'] = hours
	P1['tickets_per_hour'] = tickets_per_hour
	
	return P1


def getLaw(address):
		from django.db import connection, transaction
		longlat = getPoint(address)
		longlat = longlat + longlat
		cursor = connection.cursor()
		sql = '''select violation, violation_description as description, fine_amt,split_part(location, ' ', 2)
					   AS street,ROUND(MAX(ST_Distance_Sphere(geopoint,ST_SetSRID(ST_Point(%s, %s), 4269))))
					   AS meters from tickets where ST_DWithin(geopoint, ST_SetSRID(ST_Point(%s, %s), 4269),
					   0.0005) group by violation, violation_description, fine_amt, street'''
		cursor.execute(sql,longlat)
		result = dictfetchall(cursor)
		return result
	

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
