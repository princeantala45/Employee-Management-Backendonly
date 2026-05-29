    import os
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    url = "https://www.flipkart.com/"

    # Create folders
    os.makedirs("images", exist_ok=True)
    os.makedirs("fonts", exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    # Download images
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            img_url = urljoin(url, src)

            try:
                filename = os.path.basename(img_url.split("?")[0])
                response = requests.get(img_url, headers=headers)

                with open(f"images/{filename}", "wb") as f:
                    f.write(response.content)

                print("Downloaded image:", filename)

            except Exception as e:
                print("Image error:", e)

    # Find CSS files
    for link in soup.find_all("link", rel="stylesheet"):
        css_url = urljoin(url, link.get("href"))

        try:
            css = requests.get(css_url, headers=headers).text

            # Find font URLs
            import re
            font_urls = re.findall(r'url\(["\']?(.*?)["\']?\)', css)

            for font_url in font_urls:
                if any(ext in font_url.lower() for ext in [".woff", ".woff2", ".ttf", ".otf"]):
                    full_font_url = urljoin(css_url, font_url)
                    filename = os.path.basename(full_font_url.split("?")[0])

                    font_data = requests.get(full_font_url, headers=headers).content

                    with open(f"fonts/{filename}", "wb") as f:
                        f.write(font_data)

                    print("Downloaded font:", filename)

        except Exception as e:
            print("CSS/Font error:", e)