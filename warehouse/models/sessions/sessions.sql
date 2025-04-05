with source_data as (
    select 1 as id
    union all
    select 1 as speaker_id
    union all
    select 1 as title
    union all
    select 1 as summary
    union all
    select 1 as location
    union all
    select 1 as date
    union all
    select 1 as timeslot
    union all
    select 1 as duration
)
select
    *
from source_data
