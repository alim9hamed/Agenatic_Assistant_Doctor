from enum import Enum

class ResponseSignal(Enum):

    
    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_SUCCESS = "processing_success"
    PROCESSING_FAILED = "processing_failed"
    NO_FILES_RRRORS = "not_found_files"
    FILE_ID_ERROR = "no_file_found with_given_id"
    PROJECT_NOT_FOUND_ERROR = "project_not_found"
    INSERT_INIO_VERCTORDB_FAILED = "insert_into_vectordb_failed"  
    INSERT_INIO_VERCTORDB_SUCCESS = "insert_into_vectordb_success"
    VECTOR_COLLECTION_RETRIVED_SUCCESS = "vector_collection_retrived_success"
    VECTOR_SEARCH_ERORR = "vector_search_error"
    VECTOR_SEARCH_SUCCESS = "vector_search_success"
    RAG_ANSWER_ERROR = "rag_answer_error"
    RAG_ANSWER_SUCCESS = "rag_answer_success"