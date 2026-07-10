from app.runtime import runtime


if __name__ == "__main__":
    print({"organizations": len(runtime.list_collection("organizations")), "users": len(runtime.list_collection("users"))})
