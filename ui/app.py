import json
import os

import httpx
import streamlit as st

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1/generation")

def main():
    st.title("Content Generation Service")
    st.write("Generate content based on different strategies and requirements")

    # Generation Type
    generation_type = st.selectbox(
        "Generation Type",
        ["default", "claim_discovery", "evidence_discovery"]
    )

    # Output Type
    output_type = st.selectbox(
        "Output Type",
        ["json", "text"]
    )

    # Search Type
    search_type = st.selectbox(
        "Search Type",
        ["global", "selected_files"]
    )

    # Content
    content = st.text_area("Content", placeholder="Enter the content to process")

    # JSON Schema (if output type is JSON)
    output_schema = None
    if output_type == "json":
        schema_text = st.text_area(
            "Output Schema (Required for JSON output)",
            placeholder='{"type": "object", "properties": {...}}'
        )
        if schema_text:
            try:
                output_schema = json.loads(schema_text)
            except json.JSONDecodeError:
                st.error("Invalid JSON schema format")

    # Additional Parameters
    additional_params = st.text_area(
        "Additional Parameters (JSON format, Optional)",
        placeholder='{"key": "value"}'
    )

    if st.button("Generate"):
        try:
            # Prepare request data
            request_data = {
                "generation_type": generation_type,
                "output_type": output_type,
                "search_type": search_type,
                "parameters": {
                    "content": content
                }
            }

            # Add output schema if JSON output type
            if output_type == "json":
                if not output_schema:
                    st.error("Output schema is required for JSON output type")
                    return
                request_data["output_schema"] = output_schema

            # Add additional parameters if provided
            if additional_params:
                try:
                    additional = json.loads(additional_params)
                    request_data["parameters"].update(additional)
                except json.JSONDecodeError:
                    st.error("Invalid additional parameters format")
                    return

            # Make API request
            with httpx.Client() as client:
                response = client.post(f"{API_URL}/generate", json=request_data)
                response.raise_for_status()
                result = response.json()

            # Display results
            st.subheader("Generated Content")
            st.write(result["content"])
            
            st.subheader("Metadata")
            st.json(result["metadata"])

            if "search_results" in result:
                st.subheader("Search Results")
                st.json(result["search_results"])

        except httpx.HTTPStatusError as e:
            st.error(f"API Error: {e.response.json()['detail']}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 