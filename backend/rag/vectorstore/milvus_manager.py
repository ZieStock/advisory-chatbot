from pymilvus import MilvusClient, DataType

class MilvusManager:
    def __init__(self, collection_name = 'news'):
        self.client = MilvusClient()
        self.collection_name = collection_name
    def get_or_create_collection(self):
        if self.client.has_collection(self.collection_name):
            self.client.load_collection(self.collection_name)
            return self.client
        schema = self.client.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field(field_name = 'id', datatype = DataType.INT64, is_primary = True)
        schema.add_field(field_name='title', datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name='link', datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name='symbol', datatype=DataType.VARCHAR, max_length=50)
        schema.add_field(field_name = 'content', datatype = DataType.VARCHAR, max_length = 60000)
        schema.add_field(field_name='published_at', datatype=DataType.INT64)
        schema.add_field(field_name = 'vector', datatype = DataType.FLOAT_VECTOR, dim = 384)
        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name="vector",
            metric_type= "COSINE",
            index_type="IVF_FLAT",
            params={"nlist": 384}
        )
        self.client.create_collection(collection_name=self.collection_name, schema=schema,index_params=index_params, properties={"collection.ttl.seconds": 31536000})
        return self.client.load_collection(self.collection_name)
    def insert_data(self, data: list):
        return self.client.insert(self.collection_name, data)