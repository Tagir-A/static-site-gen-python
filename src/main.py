from textnode import TextNode, TextType


def main():
    test = TextNode("hello", TextType.LINK, "https://www.boot.dev")
    print(test)
    # print(f"{None}")


main()
