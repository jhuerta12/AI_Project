from typing import Dict, List, Set

products = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "category": "Electronics",
        "tags": ["wireless", "mouse", "accessory", "computer"],
    },
    {
        "id": 2,
        "name": "Bluetooth Headphones",
        "category": "Electronics",
        "tags": ["wireless", "headphones", "audio", "music"],
    },
    {
        "id": 3,
        "name": "Running Shoes",
        "category": "Sports",
        "tags": ["shoes", "running", "fitness", "athletic"],
    },
    {
        "id": 4,
        "name": "Water Bottle",
        "category": "Sports",
        "tags": ["hydration", "bottle", "fitness", "outdoor"],
    },
    {
        "id": 5,
        "name": "Laptop Stand",
        "category": "Office",
        "tags": ["computer", "ergonomic", "office", "desk"],
    },
    {
        "id": 6,
        "name": "Notebook",
        "category": "Office",
        "tags": ["paper", "stationery", "office", "writing"],
    },
]

user_histories: Dict[str, List[int]] = {
    "alice": [1, 5],
    "bob": [2, 4],
    "carol": [3, 4],
}

_product_tag_map: Dict[int, Set[str]] = {}


def build_product_tag_map() -> None:
    global _product_tag_map
    _product_tag_map = {
        product["id"]: set(product["tags"]) | {product["category"].lower()}
        for product in products
    }


def product_similarity(product_id_a: int, product_id_b: int) -> float:
    tags_a = _product_tag_map.get(product_id_a, set())
    tags_b = _product_tag_map.get(product_id_b, set())
    if not tags_a or not tags_b:
        return 0.0
    intersection = tags_a & tags_b
    union = tags_a | tags_b
    return len(intersection) / len(union)


def recommend_products(user_id: str, top_n: int = 5) -> List[Dict]:
    purchased = set(user_histories.get(user_id, []))
    candidate_products = [p for p in products if p["id"] not in purchased]
    if not purchased or not candidate_products:
        return candidate_products

    scored_products = []
    for candidate in candidate_products:
        candidate_id = candidate["id"]
        similarities = [product_similarity(candidate_id, purchased_id) for purchased_id in purchased]
        average_similarity = sum(similarities) / len(similarities)
        scored_products.append((average_similarity, candidate))

    scored_products.sort(key=lambda item: item[0], reverse=True)
    return [product for _, product in scored_products[:top_n]]


def display_recommendations(user_id: str, count: int = 5) -> None:
    recommendations = recommend_products(user_id, count)
    print(f"Recommendations for {user_id}:")
    if not recommendations:
        print("  No recommendations available.")
        return
    for product in recommendations:
        print(f"  - {product['name']} ({product['category']})")


if __name__ == "__main__":
    build_product_tag_map()
    display_recommendations("alice")
    display_recommendations("bob")
    display_recommendations("carol")


