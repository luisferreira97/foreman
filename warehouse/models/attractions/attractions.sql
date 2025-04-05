with source_data as (
  select 'type' as type
  union all
  select 'type' as name
  union all
  select 'type' as short_description
  union all
  select 'type' as address
  union all
  select 10 as discount
)
select
    *
from source_data
