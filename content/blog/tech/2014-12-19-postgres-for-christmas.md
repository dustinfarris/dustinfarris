Title: Santa Delivered Postgres 9.4
Tags: PostgreSQL
Summary: This year we unwrapped the JSONB data type

[PostgreSQL 9.4 Increases Flexibility, Scalability and Performance][1]:

> With the new JSONB data type for PostgreSQL, users no longer have to choose between relational
> and non-relational data stores: they can have both at the same time. JSONB supports fast lookups
> and simple expression search queries using Generalized Inverted Indexes (GIN). Multiple new
> support functions enable users to extract and manipulate JSON data, with a performance which
> matches or surpasses the most popular document databases.

I've been using PostgreSQL for a very long time, and have long resisted the NoSQL movement.  In
recent weeks, however, I've been seriously contemplating the use of Elasticsearch as a full-fledged
persistent store.  Christmas responded by dropping a [new data type][2] for Postgres in my lap.


[1]: http://www.postgresql.org/about/news/1557/
[2]: http://www.postgresql.org/docs/9.4/static/datatype-json.html
