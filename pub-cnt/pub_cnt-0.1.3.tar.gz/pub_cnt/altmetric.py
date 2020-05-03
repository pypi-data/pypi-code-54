import logging
import requests, json
import pandas as pd
import sys

def parse_data(data, keys):
  try:
    for key in keys:
      data = data[key]
    return [data]
  except:
    return 'Not Available'

def construct_data_frame(data):
  get_value = lambda field: [data[field]] if field in data.keys() else 'Not Available'
  
  df = pd.DataFrame({
    'title': get_value('title'),
    'journal': get_value('journal'),
    'doi': get_value('doi'),
    'pmid': get_value('pmid'),
    'published_on': get_value('published_on'),
    'score': get_value('score'),
    'one_year_old_score': parse_data(data, ['history', '1y']),
    'readers_count': get_value('readers_count'),
    'cited_by_posts_count': get_value('cited_by_posts_count'),
    'cited_by_tweeters_count': get_value('cited_by_tweeters_count'),
    'cited_by_feeds_count': get_value('cited_by_feeds_count'),
    'cited_by_msm_count': get_value('cited_by_msm_count'),
    'cited_by_accounts_count': get_value('cited_by_accounts_count'),
    'type': get_value('type'),
    'altmetric_id': get_value('altmetric_id'),
    'publication_url': get_value('url')
  })
  
  return df

def get_url(doi, pmid):
  construct_url = lambda parameter, _id: 'https://api.altmetric.com/v1/%s/%s' % (parameter, str(_id))
  
  if doi:
    return construct_url('doi', doi)
  else:
    return construct_url('pmid', pmid)

def get_data(doi = None, pmid = None):
  try:
    if not doi and not pmid:
      logging.error('doi or pubmed id must be provided')
      return
    
    response = requests.get(get_url(doi, pmid), headers = {'Accept': 'application/json'})
    
    if response.status_code == 200:
      try:
        json_data = json.loads(response.text.encode('utf-8'))
      except:
        logging.error("json data not available")
        return
      
      return construct_data_frame(json_data)
    
    else:
      logging.error('Response Error: %s', response.status_code)
  
  except:
    logging.error('Error occurred unavailable due to %s' % sys.exc_info()[0].__name__)
