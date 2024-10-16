from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import os
import time
from dotenv import load_dotenv
load_dotenv() 


class OpenaiApi:
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
    DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")
    MODEL = os.getenv("OPENAI_MODEL")
    API_VERSION = os.getenv("OPENAI_API_VERSION")
    MAX_RETRY = 3


    def __init__(self):
        self.llm = AzureChatOpenAI(deployment_name=self.DEPLOYMENT,
                            model=self.MODEL,
                            openai_api_version=self.API_VERSION,
                            openai_api_base=self.OPENAI_API_BASE)


    def _is_valid_json(self, input: str):
        """Check whether input string is valid JSON or not

        :param input: input string

        :returns: boolean value on validation check
        """
        try:
            json.loads(input)
            valid_flag = True
        except ValueError as e:
            valid_flag = False

        return valid_flag


    def _run_chain(self, chain: LLMChain, params: dict):
        retry_count = 0

        while retry_count < self.MAX_RETRY:
            response = chain(params)
            if self._is_valid_json(response["text"]):
                return response["text"]
            print(f"[ERROR] Got bad format response from LLM: {response['text']}")
            retry_count += 1

        raise ValueError("Got bad format response from LLM")


    def recommend_data_processing_scenario(self, industry_name: str):
        recommend_data_processing_scenario_template = """
        You're a data engineer and familiar with the {industry_name} industry IT systems.
        Please recommend 7 to 10 different data processing pipelines scenarios, including required steps like collecting data sources, transforming the data and generating aggregated metrics, etc.
        Your answer should be in an array of JSON format like below.
        [
            {{
                "pipeline_name": "{{name of the data processing pipeline}}",
                "description": "{{short description on the data pipeline}}",
                "stages": [
                    {{
                        "stage": "staging",
                        "description": "{{description on collected data sources for the rest of the data processing pipeline}}"
                    }},
                    {{
                        "stage": "standard",
                        "description": "{{description on data transformation logics}}"
                    }},
                    {{
                        "stage": "serving",
                        "description": "{{description on data aggregation logics}}"
                    }}
                ]
            }}
        ]
        Therefore your answers are:
        """

        prompt = PromptTemplate(
            input_variables=["industry_name"],
            template=recommend_data_processing_scenario_template,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        results = self._run_chain(chain, {"industry_name": industry_name})

        return results


    def recommend_tables_for_industry(self, industry_name: str, industry_contexts: str):
        """ Recommend database tables for a given industry and relevant contexts.

        :param industry_name: industry name
        :param industry_contexts: industry descriptions/contexts

        :returns: recommened tables with schema in array of json format
        """

        recommaned_tables_for_industry_template = """
        You're a data engineer and familiar with the {industry_name} industry IT systems.
        And below is relevant contexts of the industry:
        {industry_contexts}

        Please recommend some database tables with potential data schema for the above contexts.
        Your response should be an array of JSON format objects like below.
        {{
            "table_name": "{{table name}}",
            "table_description": "{{table description}}",
            "columns": [
                {{
                    "column_name": "{{column name}}",
                    "data_type": "{{data type}}",
                    "is_null": {{true or false}},
                    "is_primary_key": {{true or false}},
                    "is_foreign_key": {{true or false}}
                }}
            ]
        }}
        
        Please recommend 7 to 10 database tables:
        """

        prompt = PromptTemplate(
            input_variables=["industry_name", "industry_contexts"],
            template=recommaned_tables_for_industry_template,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        results = self._run_chain(chain, {"industry_name": industry_name,
                                           "industry_contexts": industry_contexts})

        return results


    def recommend_data_processing_scenario_mock(self, industry_name: str):
        results = """
        [ { "pipeline_name": "Flight Delay Pipeline", "description": "Collects flight data from various sources and generates metrics on delays", "stages": [ { "stage": "staging", "description": "Collects flight data from airline APIs and airport databases" }, { "stage": "standard", "description": "Transforms data to calculate delay metrics based on departure and arrival times" }, { "stage": "serving", "description": "Aggregates delay metrics by airport, airline, and route" } ] }, { "pipeline_name": "Baggage Handling Pipeline", "description": "Tracks baggage movement and generates metrics on handling efficiency", "stages": [ { "stage": "staging", "description": "Collects baggage movement data from RFID scanners and baggage handling systems" }, { "stage": "standard", "description": "Transforms data to calculate metrics on baggage handling efficiency, such as time to load and unload baggage" }, { "stage": "serving", "description": "Aggregates metrics by airport, airline, and baggage handling company" } ] }, { "pipeline_name": "Revenue Management Pipeline", "description": "Analyzes sales data to optimize pricing and revenue", "stages": [ { "stage": "staging", "description": "Collects sales data from ticketing systems and travel booking websites" }, { "stage": "standard", "description": "Transforms data to calculate revenue metrics, such as average ticket price and revenue per seat" }, { "stage": "serving", "description": "Aggregates metrics by route, fare class, and seasonality" } ] }, { "pipeline_name": "Maintenance Pipeline", "description": "Monitors aircraft health and schedules maintenance", "stages": [ { "stage": "staging", "description": "Collects aircraft sensor data and maintenance records" }, { "stage": "standard", "description": "Transforms data to identify potential maintenance issues and schedule preventative maintenance" }, { "stage": "serving", "description": "Aggregates metrics by aircraft type, age, and maintenance history" } ] }, { "pipeline_name": "Customer Service Pipeline", "description": "Analyzes customer feedback to improve service", "stages": [ { "stage": "staging", "description": "Collects customer feedback from surveys, social media, and customer service interactions" }, { "stage": "standard", "description": "Transforms data to identify common issues and sentiment analysis of customer feedback" }, { "stage": "serving", "description": "Aggregates metrics by route, airline, and customer feedback channel" } ] }, { "pipeline_name": "Fuel Efficiency Pipeline", "description": "Monitors fuel usage to optimize efficiency and reduce costs", "stages": [ { "stage": "staging", "description": "Collects fuel usage data from aircraft sensors and fueling systems" }, { "stage": "standard", "description": "Transforms data to calculate fuel efficiency metrics, such as fuel burn per passenger mile" }, { "stage": "serving", "description": "Aggregates metrics by aircraft type, route, and seasonality" } ] }, { "pipeline_name": "Security Pipeline", "description": "Monitors security incidents to improve safety and compliance", "stages": [ { "stage": "staging", "description": "Collects security incident data from airport security systems and passenger screening" }, { "stage": "standard", "description": "Transforms data to identify common security incidents and compliance issues" }, { "stage": "serving", "description": "Aggregates metrics by airport, airline, and security incident type" } ] } ]
        """

        return results


    def recommend_tables_for_industry_mock(self, industry_name: str, industry_contexts: str):
        results = """
        [{"table_name":"airlines","table_description":"Information about the airline companies","columns":[{"column_name":"airline_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"name","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"country","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false}]},{"table_name":"flights","table_description":"Information about flights operated by airlines","columns":[{"column_name":"flight_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"airline_id","data_type":"integer","is_null":false,"is_primary_key":false,"is_foreign_key":true},{"column_name":"origin","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"destination","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"departure_time","data_type":"datetime","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"arrival_time","data_type":"datetime","is_null":false,"is_primary_key":false,"is_foreign_key":false}]},{"table_name":"passengers","table_description":"Information about passengers","columns":[{"column_name":"passenger_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"name","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"age","data_type":"integer","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"gender","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"flight_id","data_type":"integer","is_null":false,"is_primary_key":false,"is_foreign_key":true}]},{"table_name":"bookings","table_description":"Information about flight bookings made by passengers","columns":[{"column_name":"booking_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"passenger_id","data_type":"integer","is_null":false,"is_primary_key":false,"is_foreign_key":true},{"column_name":"flight_id","data_type":"integer","is_null":false,"is_primary_key":false,"is_foreign_key":true}]},{"table_name":"seats","table_description":"Information about seats available in flights","columns":[{"column_name":"seat_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"flight_id","data_type":"integer","is_null":false,"is_primary_key":false,"is_foreign_key":true},{"column_name":"passenger_id","data_type":"integer","is_null":true,"is_primary_key":false,"is_foreign_key":true},{"column_name":"seat_number","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false}]},{"table_name":"airports","table_description":"Information about airports","columns":[{"column_name":"airport_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"name","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"location","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false}]}]
        """

        return results


    def recommend_tables_for_industry_one_at_a_time(self, industry_name: str, industry_contexts: str, recommended_tables: str = None, index: int = None):
        recommaned_tables_for_industry_template = """
        You're a data engineer and familiar with the {industry_name} industry IT systems.
        And below is relevant contexts of the industry:
        {industry_contexts}

        Please recommend some database tables with potential data schema for the above contexts.
        Your response should strictly be in JSON format like below.
        {{
            "table_name": "{{table name}}",
            "table_description": "{{table description}}",
            "columns": [
                {{
                    "column_name": "{{column name}}",
                    "data_type": "{{data type}}",
                    "is_null": {{true or false (strictly in lower case)}},
                    "is_primary_key": {{true or false (strictly in lower case)}},
                    "is_foreign_key": {{true or false (strictly in lower case)}}
                }}
            ]
        }}

        You've recommanded below tables in previous conversations.
        {recommended_tables}

        Please recommend another one without duplicated table (if there's no table listed above, please go ahead to create a new one):
        """

        prompt = PromptTemplate(
            input_variables=["industry_name", "industry_contexts", "recommended_tables"],
            template=recommaned_tables_for_industry_template,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        results = self._run_chain(chain, {"industry_name": industry_name,
                                           "industry_contexts": industry_contexts,
                                           "recommended_tables": recommended_tables})

        return results


    def recommend_tables_for_industry_one_at_a_time_mock(self, industry_name: str, industry_contexts: str, index: int):
        if index == 0:
            results = """
            {"table_name":"flights","table_description":"Table to store information about flights","columns":[{"column_name":"flight_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"airline_id","data_type":"integer","is_null":false,"is_primary_key":false,"is_foreign_key":true},{"column_name":"departure_city","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"arrival_city","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"departure_date","data_type":"date","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"departure_time","data_type":"time","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"arrival_date","data_type":"date","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"arrival_time","data_type":"time","is_null":false,"is_primary_key":false,"is_foreign_key":false}]}
            """
        elif index == 1:
            results = """
            {"table_name":"passengers","table_description":"Table to store information about passengers","columns":[{"column_name":"passenger_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"passenger_name","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"date_of_birth","data_type":"date","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"email","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"phone_number","data_type":"varchar(20)","is_null":true,"is_primary_key":false,"is_foreign_key":false}]}
            """
        elif index == 2:
            results = """
            {"table_name":"airlines","table_description":"Table to store information about airline companies","columns":[{"column_name":"airline_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"airline_name","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"country","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false}]}
            """
        elif index == 3:
            results = """
            {"table_name":"tickets","table_description":"Table to store information about airline tickets","columns":[{"column_name":"ticket_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"passenger_id","data_type":"integer","is_null":false,"is_primary_key":false,"is_foreign_key":true},{"column_name":"flight_id","data_type":"integer","is_null":false,"is_primary_key":false,"is_foreign_key":true},{"column_name":"ticket_number","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"ticket_class","data_type":"varchar(50)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"ticket_price","data_type":"decimal(10,2)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"ticket_status","data_type":"varchar(50)","is_null":false,"is_primary_key":false,"is_foreign_key":false}]}
            """
        elif index == 4:
            results = """
            {"table_name":"airports","table_description":"Table to store information about airports","columns":[{"column_name":"airport_id","data_type":"integer","is_null":false,"is_primary_key":true,"is_foreign_key":false},{"column_name":"airport_name","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"city","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false},{"column_name":"country","data_type":"varchar(255)","is_null":false,"is_primary_key":false,"is_foreign_key":false}]}
            """
        # Simulate request consuming response time
        time.sleep(1)

        return results


    def generate_custom_data_processing_logics_mock(self,
                                                    industry_name: str,
                                                    industry_contexts: str,
                                                    involved_tables: str,
                                                    custom_data_processing_logic: str,
                                                    output_table_name: str):
        results = """
        {"sql":"SELECT flights.airline_id, flights.arrival_time, flights.departure_time, flights.destination, flights.flight_id, flights.origin, passengers.age, passengers.gender, passengers.name, passengers.passenger_id FROM flights JOIN bookings ON flights.flight_id = bookings.flight_id JOIN passengers ON bookings.passenger_id = passengers.passenger_id","schema":{"table_name":"std_flights_p","columns":[{"column_name":"airline_id","data_type":"long","is_null":true,"is_primary_key":false,"is_foreign_key":true},{"column_name":"arrival_time","data_type":"string","is_null":true,"is_primary_key":false,"is_foreign_key":false},{"column_name":"departure_time","data_type":"string","is_null":true,"is_primary_key":false,"is_foreign_key":false},{"column_name":"destination","data_type":"string","is_null":true,"is_primary_key":false,"is_foreign_key":false},{"column_name":"flight_id","data_type":"long","is_null":true,"is_primary_key":false,"is_foreign_key":true},{"column_name":"origin","data_type":"string","is_null":true,"is_primary_key":false,"is_foreign_key":false},{"column_name":"age","data_type":"long","is_null":true,"is_primary_key":false,"is_foreign_key":false},{"column_name":"gender","data_type":"string","is_null":true,"is_primary_key":false,"is_foreign_key":false},{"column_name":"name","data_type":"string","is_null":true,"is_primary_key":false,"is_foreign_key":false},{"column_name":"passenger_id","data_type":"long","is_null":true,"is_primary_key":false,"is_foreign_key":true}]}}
        """

        return results


    def recommend_custom_table(self, 
                               industry_name: str,
                               industry_contexts: str,
                               recommened_tables: str,
                               custom_table_name: str,
                               custom_table_description: str):
        """ Recommend custom/user-defined table for a input custom table name and description of a given industry.

        :param industry_name: industry name
        :param industry_contexts: industry descriptions/contexts
        :param recommened_tables: previously recommened tables in json string format
        :param custom_table_name: custom table name
        :param custom_table_description: custom table description

        :returns: recommened custom tables with schema in json format
        """

        recommend_custom_tables_template="""
        You're a data engineer and familiar with the {industry_name} industry IT systems.
        And below is relevant contexts of the industry:
        {industry_contexts}

        You've recommended below potential database tables and schema previously in json format.
        {recommened_tables}

        Please help to add another {custom_table_name} table with the same table schema format, please include as many as possible columns reflecting the reality and the table description below.
        {custom_table_description}

        Please only output the new added table without previously recommended tables, therefore the outcome would be:
        """

        prompt = PromptTemplate(
            input_variables=["industry_name", "industry_contexts", "recommened_tables", "custom_table_name", "custom_table_description"],
            template=recommend_custom_tables_template,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        results = self._run_chain(chain, {"industry_name": industry_name,
                                           "industry_contexts": industry_contexts,
                                           "recommened_tables": recommened_tables,
                                           "custom_table_name": custom_table_name,
                                           "custom_table_description": custom_table_description})

        return results


    def recommend_data_processing_logics(self,
                                         industry_name: str,
                                         industry_contexts: str,
                                         recommened_tables: str,
                                         processing_logic: str):
        """ Recommend data processing logics for a given industry and sample tables.

        :param industry_name: industry name
        :param industry_contexts: industry descriptions/contexts
        :param recommened_tables: previously recommened tables in json string format
        :param processing_logic: either data cleaning, data transformation or data aggregation

        :returns: recommened data processing logics in array of json format
        """

        recommend_data_cleaning_logics_template="""
        You're a data engineer and familiar with the {industry_name} industry IT systems.
        And below is relevant contexts of the industry:
        {industry_contexts}

        You've recommended below potential database tables and schema previously in json format.
        {recommened_tables}

        Please recommend 5 to 7 {processing_logic} logic over the above tables with Spark SQL statements.
        You response should be in an array of JSON format like below.
        {{
            "description": "{{descriptions on the data cleaning logic}}",
            "involved_tables": [
                "{{involved table X}}",
                "{{involved table Y}}",
                "{{involved table Z}}"
            ],
            "sql": "{{Spark SQL statement to do the data cleaning}}",
            "schema": "{{cleaned table schema in json string format}}"
        }}
        
        Therefore outcome would be:
        """

        prompt = PromptTemplate(
            input_variables=["industry_name", "industry_contexts", "processing_logic", "recommened_tables"],
            template=recommend_data_cleaning_logics_template,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        results = self._run_chain(chain, {"industry_name": industry_name,
                                           "industry_contexts": industry_contexts,
                                           "processing_logic": processing_logic,
                                           "recommened_tables": recommened_tables})

        return results


    def generate_custom_data_processing_logics(self,
                                               industry_name: str,
                                               industry_contexts: str,
                                               involved_tables: str,
                                               custom_data_processing_logic: str,
                                               output_table_name: str):
        """ Generate custom data processing logics for input data processing requirements.

        :param industry_name: industry name
        :param industry_contexts: industry descriptions/contexts
        :param involved_tables: tables required by the custom data processing logic, in json string format
        :param custom_data_processing_logic: custom data processing requirements
        :param output_table_name: output/sink table name for processed data

        :returns: custom data processing logic json format
        """

        generate_custom_data_processing_logics_template = """
        You're a data engineer and familiar with the {industry_name} industry IT systems.
        And below is relevant contexts of the industry:
        {industry_contexts}

        We have database tables listed below with table_name and schema in JSON format.
        {involved_tables}

        And below is the data processing requirement.
        {custom_data_processing_logic}

        Please help to generate Spark SQL statement with output data schema.
        And your response should be in JSON format like below.
        {{
            "sql": "{{Spark SQL statement to do the data cleaning}}",
            "schema": "{{output data schema in JSON string format}}"
        }}

        And the above data schema string should follows below JSON format, while value for the "table_name" key should strictly be "{output_table_name}".
        {{
            "table_name": "{output_table_name}",
            "coloumns": [
                {{
                    "column_name": "{{column name}}",
                    "data_type": "{{data type}}",
                    "is_null": {{true or false}},
                    "is_primary_key": {{true or false}},
                    "is_foreign_key": {{true or false}}
                }}
            ]
        }}

        Therefore the outcome would be:
        """

        prompt = PromptTemplate(
            input_variables=["industry_name", "industry_contexts", "involved_tables", "custom_data_processing_logic", "output_table_name"],
            template=generate_custom_data_processing_logics_template,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)

        # Run the chain only specifying the input variable.
        results = self._run_chain(chain, {"industry_name": industry_name,
                                           "industry_contexts": industry_contexts,
                                           "custom_data_processing_logic": custom_data_processing_logic,
                                           "involved_tables": involved_tables,
                                           "output_table_name": output_table_name})

        return results


    def generate_sample_data(self,
                             industry_name: str,
                             number_of_lines: int,
                             target_table: str,
                             column_values_patterns: str):
        """ Generate custom data processing logics for input data processing requirements.

        :param industry_name: industry name
        :param number_of_lines: number of lines sample data required
        :param target_table: target table name and its schema in json format

        :returns: generated sample data in array of json format
        """

        generate_sample_data_template = """
        You're a data engineer and familiar with the {industry_name} industry IT systems.
        Please help to generate {number_of_lines} lines of sample data for below table with table schema in json format.
        {target_table}

        And below are patterns of column values in json format, if it's not provided please ignore this requirement.
        {column_values_patterns}

        And the sample data should strictly be in JSON format like below.
        [
            {{
                "{{column X}}": "{{column value}}",
                "{{column Y}}": "{{column value}}",
                "{{column Z}}": "{{column value}}"
            }}
        ]

        Therefore the sample data would be:
        """

        prompt = PromptTemplate(
            input_variables=["industry_name", "number_of_lines", "target_table", "column_values_patterns"],
            template=generate_sample_data_template,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        results = self._run_chain(chain, {"industry_name": industry_name,
                                           "number_of_lines": number_of_lines,
                                           "target_table": target_table,
                                           "column_values_patterns": column_values_patterns})

        return results


    def generate_sample_data_mock(self,
                                  industry_name: str,
                                  number_of_lines: int,
                                  target_table: str,
                                  column_values_patterns: str):
        if target_table["table_name"] == "flights":
            results = """
            [ { "flight_id": 1, "airline_id": 1001, "origin": "New York", "destination": "Los Angeles", "departure_time": "2021-01-01 08:00:00", "arrival_time": "2021-01-01 11:30:00" }, { "flight_id": 2, "airline_id": 1002, "origin": "London", "destination": "Paris", "departure_time": "2021-01-02 14:30:00", "arrival_time": "2021-01-02 16:00:00" }, { "flight_id": 3, "airline_id": 1003, "origin": "Tokyo", "destination": "Sydney", "departure_time": "2021-01-03 10:45:00", "arrival_time": "2021-01-04 06:15:00" }, { "flight_id": 4, "airline_id": 1004, "origin": "Chicago", "destination": "Miami", "departure_time": "2021-01-05 16:20:00", "arrival_time": "2021-01-05 19:45:00" }, { "flight_id": 5, "airline_id": 1005, "origin": "Sydney", "destination": "Melbourne", "departure_time": "2021-01-06 09:15:00", "arrival_time": "2021-01-06 10:30:00" }, { "flight_id": 6, "airline_id": 1001, "origin": "Los Angeles", "destination": "New York", "departure_time": "2021-01-07 12:00:00", "arrival_time": "2021-01-07 15:30:00" }, { "flight_id": 7, "airline_id": 1002, "origin": "Paris", "destination": "London", "departure_time": "2021-01-08 18:45:00", "arrival_time": "2021-01-08 20:15:00" }, { "flight_id": 8, "airline_id": 1003, "origin": "Sydney", "destination": "Tokyo", "departure_time": "2021-01-09 14:30:00", "arrival_time": "2021-01-10 08:00:00" }, { "flight_id": 9, "airline_id": 1004, "origin": "Miami", "destination": "Chicago", "departure_time": "2021-01-11 20:00:00", "arrival_time": "2021-01-11 23:25:00" }, { "flight_id": 10, "airline_id": 1005, "origin": "Melbourne", "destination": "Sydney", "departure_time": "2021-01-12 13:45:00", "arrival_time": "2021-01-12 15:00:00" }, { "flight_id": 11, "airline_id": 1001, "origin": "New York", "destination": "Los Angeles", "departure_time": "2021-01-13 08:00:00", "arrival_time": "2021-01-13 11:30:00" }, { "flight_id": 12, "airline_id": 1002, "origin": "London", "destination": "Paris", "departure_time": "2021-01-14 14:30:00", "arrival_time": "2021-01-14 16:00:00" }, { "flight_id": 13, "airline_id": 1003, "origin": "Tokyo", "destination": "Sydney", "departure_time": "2021-01-15 10:45:00", "arrival_time": "2021-01-16 06:15:00" }, { "flight_id": 14, "airline_id": 1004, "origin": "Chicago", "destination": "Miami", "departure_time": "2021-01-17 16:20:00", "arrival_time": "2021-01-17 19:45:00" }, { "flight_id": 15, "airline_id": 1005, "origin": "Sydney", "destination": "Melbourne", "departure_time": "2021-01-18 09:15:00", "arrival_time": "2021-01-18 10:30:00" }, { "flight_id": 16, "airline_id": 1001, "origin": "Los Angeles", "destination": "New York", "departure_time": "2021-01-19 12:00:00", "arrival_time": "2021-01-19 15:30:00" }, { "flight_id": 17, "airline_id": 1002, "origin": "Paris", "destination": "London", "departure_time": "2021-01-20 18:45:00", "arrival_time": "2021-01-20 20:15:00" }, { "flight_id": 18, "airline_id": 1003, "origin": "Sydney", "destination": "Tokyo", "departure_time": "2021-01-21 14:30:00", "arrival_time": "2021-01-22 08:00:00" }, { "flight_id": 19, "airline_id": 1004, "origin": "Miami", "destination": "Chicago", "departure_time": "2021-01-23 20:00:00", "arrival_time": "2021-01-23 23:25:00" }, { "flight_id": 20, "airline_id": 1005, "origin": "Melbourne", "destination": "Sydney", "departure_time": "2021-01-24 13:45:00", "arrival_time": "2021-01-24 15:00:00" } ]
            """

        if target_table["table_name"] == "passengers":
            results = """
            [ { "passenger_id": 1, "name": "John Smith", "age": 35, "gender": "Male", "flight_id": 1 }, { "passenger_id": 2, "name": "Jane Doe", "age": 45, "gender": "Female", "flight_id": 1 }, { "passenger_id": 3, "name": "Michael Johnson", "age": 60, "gender": "Male", "flight_id": 2 }, { "passenger_id": 4, "name": "Emily Williams", "age": 25, "gender": "Female", "flight_id": 3 }, { "passenger_id": 5, "name": "David Brown", "age": 55, "gender": "Male", "flight_id": 4 }, { "passenger_id": 6, "name": "Sarah Davis", "age": 30, "gender": "Female", "flight_id": 4 }, { "passenger_id": 7, "name": "Robert Martinez", "age": 65, "gender": "Male", "flight_id": 5 }, { "passenger_id": 8, "name": "Jessica Thomas", "age": 40, "gender": "Female", "flight_id": 5 }, { "passenger_id": 9, "name": "Christopher Wilson", "age": 50, "gender": "Male", "flight_id": 1 }, { "passenger_id": 10, "name": "Stephanie Taylor", "age": 27, "gender": "Female", "flight_id": 2 }, { "passenger_id": 11, "name": "Daniel Anderson", "age": 65, "gender": "Male", "flight_id": 3 }, { "passenger_id": 12, "name": "Melissa Thompson", "age": 42, "gender": "Female", "flight_id": 4 }, { "passenger_id": 13, "name": "Matthew White", "age": 32, "gender": "Male", "flight_id": 5 }, { "passenger_id": 14, "name": "Amanda Harris", "age": 52, "gender": "Female", "flight_id": 1 }, { "passenger_id": 15, "name": "Andrew Lee", "age": 65, "gender": "Male", "flight_id": 2 }, { "passenger_id": 16, "name": "Jennifer Clark", "age": 28, "gender": "Female", "flight_id": 3 }, { "passenger_id": 17, "name": "James Rodriguez", "age": 62, "gender": "Male", "flight_id": 4 }, { "passenger_id": 18, "name": "Nicole Walker", "age": 38, "gender": "Female", "flight_id": 5 }, { "passenger_id": 19, "name": "Ryan Wright", "age": 47, "gender": "Male", "flight_id": 1 }, { "passenger_id": 20, "name": "Lauren Hall", "age": 31, "gender": "Female", "flight_id": 2 } ]
            """
        
        if target_table["table_name"] == "bookings":
            results = """
            [ { "booking_id": 1, "passenger_id": 1, "flight_id": 1 }, { "booking_id": 2, "passenger_id": 2, "flight_id": 2 }, { "booking_id": 3, "passenger_id": 3, "flight_id": 3 }, { "booking_id": 4, "passenger_id": 4, "flight_id": 4 }, { "booking_id": 5, "passenger_id": 5, "flight_id": 5 }, { "booking_id": 6, "passenger_id": 1, "flight_id": 2 }, { "booking_id": 7, "passenger_id": 2, "flight_id": 3 }, { "booking_id": 8, "passenger_id": 3, "flight_id": 4 }, { "booking_id": 9, "passenger_id": 4, "flight_id": 5 }, { "booking_id": 10, "passenger_id": 5, "flight_id": 1 }, { "booking_id": 11, "passenger_id": 1, "flight_id": 3 }, { "booking_id": 12, "passenger_id": 2, "flight_id": 4 }, { "booking_id": 13, "passenger_id": 3, "flight_id": 5 }, { "booking_id": 14, "passenger_id": 4, "flight_id": 1 }, { "booking_id": 15, "passenger_id": 5, "flight_id": 2 }, { "booking_id": 16, "passenger_id": 1, "flight_id": 4 }, { "booking_id": 17, "passenger_id": 2, "flight_id": 5 }, { "booking_id": 18, "passenger_id": 3, "flight_id": 1 }, { "booking_id": 19, "passenger_id": 4, "flight_id": 2 }, { "booking_id": 20, "passenger_id": 5, "flight_id": 3 } ]
            """

        return results
