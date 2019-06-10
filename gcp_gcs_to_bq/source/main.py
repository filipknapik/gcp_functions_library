from google.cloud import bigquery
from flask import jsonify

def execute(request):
    request_json = request.get_json()
    client = bigquery.Client()
    
    dataset = request_json['dataset']
    source = request_json['source']
    table = request_json['table']
    
    dataset_ref = client.dataset(dataset)
    job_config.skip_leading_rows = 1
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.source_format = bigquery.SourceFormat.CSV

    load_job = client.load_table_from_uri(
        source, dataset_ref.table(table), job_config=job_config
    )  
    print("Starting job {}".format(load_job.job_id))
    load_job.result()  # Waits for table load to complete.
    print("Job finished.")
    return jsonify({"Result":"OK"})