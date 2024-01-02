from typing import Optional
from fastapi import FastAPI
from models.visitors import Visitor
import uvicorn
from datetime import datetime, date, timedelta
import pandas as pd
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models.visit import Entry,Visit
from models.visitors import Visitor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_visitors_from_tsv(file_path: str) -> list[Visitor]:
    """
    Create Visitor instances from a TSV file.

    Args:
    - file_path (str): Path to the TSV file.

    Returns:
    - list[Visitor]: List of Visitor instances created from the TSV data.
    """
    try:
        data = pd.read_csv(file_path, sep='\t')
        grouped = data.groupby('propulso_id')

        visitors = []
        for visitor_id, group in grouped:
            entries = []
            for _, row in group.iterrows():
                entry_date = datetime.strptime(row['date'], "%Y-%m-%d").date()
                entry = Entry(row['propulso_id'], row['lat'], row['lng'], row['delta_time'], entry_date, row['time'])
                entries.append(entry)

            visits = []
            visit_entries = []

            for entry in entries:
                if entry.delta_time == 0:
                    visit_entries.append(entry)
                else:
                    if visit_entries:
                        visits.append(Visit(visit_entries))
                        visit_entries = []

            if visit_entries:  # Check for remaining visit entries
                visits.append(Visit(visit_entries))

            visitor = Visitor(visitor_id, visits)
            visitors.append(visitor)
        return visitors
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        return []
    except pd.errors.EmptyDataError as e:
        print(f"Empty data error: {e}")
        return []
    except pd.errors.ParserError as e:
        print(f"Parser error: {e}")
        return []

visitor_list: list[Visitor] = create_visitors_from_tsv('dataset_before_after.tsv')

@app.get("/store/1/visitor/{id}/visits")
def store_visitor_visits(id: str) -> JSONResponse:
    try:
        visitor = next((v for v in visitor_list if v.visitor_id == id), None)
        if visitor:
            return JSONResponse(content=jsonable_encoder(visitor.visits), status_code=200)
        else:
            return JSONResponse(content="Visitor not found", status_code=404)
    except Exception as e:
        return JSONResponse(content=str(e), status_code=500)


@app.get("/store/1/visitors")
def store_visitors(page: Optional[int] = 1, page_size: Optional[int] = 10) -> JSONResponse:
    try:
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_visitors: [Visitor] = visitor_list[start_index:end_index]

        return JSONResponse(content=jsonable_encoder({"paginated_visitors": paginated_visitors, "total_visitors":len(visitor_list) }), status_code=200)
    except Exception as e:
        return JSONResponse(content=str(e), status_code=500)

@app.get("/store/1/statistics/{date}")
def store_statistics(date: str) -> JSONResponse:
    try:
        date_to_check = datetime.strptime(date, "%Y-%m-%d").date()
        avg_time_visit_cumulation = timedelta()
        total_daily_visits = 0
        total_daily_visitors = 0
        for visitor in visitor_list:
            visits_count = visitor.daily_visit(date_to_check)
            total_daily_visits += visits_count
            if visits_count != 0:
                total_daily_visitors += 1
            # Calculate average time spent in the store
            avg_time_visit_cumulation += visitor.average_time_visit()
        avg_time_visit = avg_time_visit_cumulation / len(visitor_list)

        return JSONResponse(content={
            "average_time_visit": str(avg_time_visit),
            "total_daily_visits": total_daily_visits,
            "total_daily_visitors": total_daily_visitors
        }, status_code=200)
    except ValueError:
        return JSONResponse(content="Invalid date format. Please provide the date in YYYY-MM-DD format",
                            status_code=400)
    except Exception as e:
        return JSONResponse(content=str(e), status_code=500)


@app.get("/docs")
async def get_documentation():
    return {
        "message": "Welcome to the Swagger documentation!"
    }


if __name__ == "__main__":

    visitor_list = visitor_list
    print(visitor_list)
    uvicorn.run(app, host="localhost", port=3000)
