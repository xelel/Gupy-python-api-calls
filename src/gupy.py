from ast import While
from typing import List, Union, Tuple, Dict, NewType, Callable, Sequence, Iterable,Any
import logging
from urllib import response
import requests
import pandas as pd
from datetime import timedelta,datetime,timezone
import time
import os



class Gupy:
    """
    A class to interact with the Gupy API, facilitating the fetching and organization 
    of data into pandas dataframes.
    
    Attributes
    ----------
    headers : dict
        Headers to be used in the API requests, containing authorization details and 
        the expected content type.
    """
    
    def __init__(self):
        """
        Initialize a new instance of the Gupy class, setting the headers 
        for the HTTP requests made to the Gupy API.
        """
        self.token=os.environ['gupy_token']
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

    
       
    
    def fetch_requests(self, url:str,params:dict={}) -> List[Dict]:
        """
        Fetch data from a specific Gupy API endpoint.

        Parameters:
        url (str): The API endpoint URL.
        params (dict, optional): Additional parameters to pass in the API request. Defaults to {}.

        Returns:
        List[Dict]: A list of dictionaries containing the JSON response data from the API.
        """
        results=[]
        api_response=self.call_to_api(url,params).json()
        total_pages=api_response.get('totalPages')
        results.extend(api_response.get('results'))
        print(total_pages)
        for page in range(2,total_pages+1):

            params['page']=page            
            api_response=self.call_to_api(url,params).json()
                      
            results.extend(api_response.get('results'))   
            

        print('-='*5)
        return results
            
    def __dict_to_dataframe(self,dictionary: Dict[str,Any])->pd.DataFrame:
        """
        Convert a dictionary to a pandas DataFrame.

        Parameters:
        dictionary (Dict[str, Any]): The dictionary to be converted.

        Returns:
        pd.DataFrame: A pandas DataFrame obtained from the dictionary.
        """
        return pd.json_normalize(dictionary)
        
    
        
    
    def call_to_api(self,url:str,params:dict) -> requests.get:       
        """
        Perform an API call to a specific Gupy API endpoint.

        This method handles various types of errors such as HTTPError, ConnectionError, Timeout, and other 
        request exceptions, and also manages the rate limits by pausing the necessary time before making a new request.

        Parameters:
        url (str): The API endpoint URL.
        params (dict): Additional parameters to pass in the API request.

        Returns:
        requests.Response: The response object obtained from the API call.
        """ 
        try:
            response=requests.get(url,params=params,headers=self.headers)
            print(response.status_code)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as errh:
            
            if response.status_code==429:
                now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                now=datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
                server_date=datetime.utcfromtimestamp(int(response.headers.get('X-RateLimit-Reset')))
                wait_time=server_date-now
                time.sleep(wait_time.seconds)
                response=requests.get(url,params=params,headers=self.headers)
                print(response.status_code)
                return response
            
            else:
                print ("Http Error:",errh)
        
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
    
      
    
    def gupy_applications(self,jobs_id):
        """
        Retrieve applications data for a specific job ID from the Gupy API.

        Parameters:
        jobs_id (str): The job ID for which to retrieve the applications data.

        Returns:
        pd.DataFrame: A pandas DataFrame containing the applications data.
        """
        params={'order':'id asc','perPage':100}
        url=f"https://api.gupy.io/api/v1/jobs/{jobs_id}/applications"
        applications=self.fetch_requests(url,params)
        
        df_app=self.__dict_to_dataframe(applications)
        return df_app
    
    def gupy_comments(self,job_id,application_id):
        """
        Fetch comments data for a specific job and application ID and convert it to a dataframe.

        Parameters
        ----------
        job_id : str
            The job ID for which to fetch the comments data.
        application_id : str
            The application ID for which to fetch the comments data.

        Returns
        -------
        pd.DataFrame
            A dataframe containing the comments data, or None if no comments are found.
        """
        url=f"https://api.gupy.io/api/v1/jobs/{job_id}/applications/{application_id}/comments"
        comments=self.fetch_requests(url)
        df_comments=None
        if comments:
            df_comments=self.__dict_to_dataframe(comments)
        return df_comments
        
    def gupy_jobs(self):
        """
        Fetch job data from the Gupy API and convert it to a dataframe.

        Returns
        -------
        pd.DataFrame
            A dataframe containing the job data.
        """
        url="https://api.gupy.io/api/v1/jobs"
        response=self.fetch_requests(url)
        df_jobs=self.__dict_to_dataframe(response)
        return df_jobs
    
    def gupy_steps(self,jobId):
        """
        Fetch job step data for a specific job ID from the Gupy API and convert it to a dataframe.

        Parameters
        ----------
        jobId : str
            The job ID for which to fetch the step data.

        Returns
        -------
        pd.DataFrame
            A dataframe containing the job step data.
        """
        params={'perPage':100,'fields':'all'}
        url=f"https://api.gupy.io/api/v1/jobs/{jobId}/steps"
        steps=self.fetch_requests(url)
        df_steps=self.__dict_to_dataframe(steps)
        return df_steps
if __name__ == "__main__":
    gupy=Gupy()
    jobs=gupy.gupy_jobs()
    df_app=pd.DataFrame()
    df_steps=pd.DataFrame()
    for _id in jobs.id:
        app=gupy.gupy_applications(_id)
        steps=gupy.gupy_steps(_id)
        df_app=pd.concat([df_app,app],ignore_index=True)
        df_steps=pd.concat([df_steps,steps],ignore_index=True)
