data = "Dune:8, Dune:9, Barbie:7, Dune:10, Barbie:9, Oppenheimer:9, Barbie:6"


def parse_ratings(data: str) -> list:
    ratings = []

    for item in data.split(","):
        title, rating = item.split(":")
        ratings.append((title.strip(), int(rating.strip())))

    return ratings


def average_rating(ratings, title) -> float:
    scores = [rating for movie, rating in ratings if movie == title]

    if not scores:
        return 0.0

    return round(sum(scores) / len(scores), 1)


def best_movie(ratings) -> str:
    titles = set(movie for movie, rating in ratings)

    return max(titles, key=lambda movie: average_rating(ratings, movie))


def rating_counts(ratings) -> dict:
    counts = {}

    for movie, rating in ratings:
        counts[movie] = counts.get(movie, 0) + 1

    return counts


# Demo
if __name__ == "__main__":
    ratings = parse_ratings(data)

    print("Parsed ratings:")
    print(ratings)

    print("\nAverage ratings:")
    print("Dune:", average_rating(ratings, "Dune"))
    print("Barbie:", average_rating(ratings, "Barbie"))
    print("Oppenheimer:", average_rating(ratings, "Oppenheimer"))
    print("Unknown:", average_rating(ratings, "Unknown"))

    print("\nBest movie:")
    print(best_movie(ratings))

    print("\nRating counts:")
    print(rating_counts(ratings))
