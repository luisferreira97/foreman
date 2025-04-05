with source_data as (
  select 1 as id
  union all
  select '' as name
  union all
  select '' as website
  union all
  select '' as tier
)
select
    *
from source_data
