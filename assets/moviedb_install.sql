COPY maps_movies(id,movie_id, imdb_id,movie_name,genre,vectors) 
FROM '/home/norbert/Desktop/moviecloud/pyRecommend/assets/movies.csv' DELIMITER ',' CSV HEADER;

COPY maps_meansize(id,size,mean,movie_id) 
FROM '/home/norbert/Desktop/moviecloud/pyRecommend/assets/meansize.csv' DELIMITER ',' CSV HEADER;

COPY maps_links(id,movie_id,url) 
FROM '/home/norbert/Desktop/moviecloud/pyRecommend/assets/links.csv' DELIMITER ',' CSV HEADER;