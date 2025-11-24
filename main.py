from baml_py import Pdf
from baml_py import Image
from baml_client.async_client import b  # from baml_client.sync_client or async_client
from baml_py import ClientRegistry, Collector
import base64
from pathlib import Path
import asyncio
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


async def run_pdf_parsing(collector: Collector):
    pdf_path = Path("sample_tables.pdf")
    b64_pdf = base64.b64encode(pdf_path.read_bytes()).decode("utf-8")

    client_registry = ClientRegistry()
    env = {"BAML_LOG": "DEBUG"}
    pdf_df = pd.DataFrame()
    # Create client with default options
    for model_name in ["Sonnet4", "Sonnet45", "Opus41", "Haiku45"]:
        client_registry.set_primary(model_name)

        my_b = b.with_options(
            collector=collector, client_registry=client_registry, env=env
        )
        pdf_result = await my_b.ExtractPDF(
            myFile=Pdf.from_base64(b64_pdf),
            baml_options={"collector": collector},
        )
        df_ = extract_result(pdf_result, collector)
        pdf_df = pd.concat([pdf_df, df_], ignore_index=True)
        # print("PDF Result:", pdf_result.tables)
        # print("Collector Usage:", collector.usage)
        # print("Collector Calls:", collector.last.calls)
        # print("PDF Collector Last Usage:", collector.last.usage)
        # print("PDF Collector Last Timing:", collector.last.timing)
    return pdf_df


async def run_img_parsing(collector: Collector):
    img_path = Path("sample_tables.png")
    b64_img = base64.b64encode(img_path.read_bytes()).decode("utf-8")

    client_registry = ClientRegistry()
    env = {"BAML_LOG": "DEBUG"}
    img_df = pd.DataFrame()
    # Create client with default options
    for model_name in ["Sonnet4", "Sonnet45", "Opus41", "Haiku45"]:
        client_registry.set_primary(model_name)

        my_b = b.with_options(
            collector=collector, client_registry=client_registry, env=env
        )
        img_result = await my_b.ExtractImg(
            myFile=Image.from_base64("image/png", b64_img),
            baml_options={"collector": collector},
        )
        df_ = extract_result(img_result, collector)
        img_df = pd.concat([img_df, df_], ignore_index=True)
        # print("IMG Result:", img_result.tables)
        # print("Collector Usage:", collector.usage)
        # print("IMG Collector Last Usage:", collector.last.usage)
        # print("IMG Collector Last Timing:", collector.last.timing)
    return img_df


def extract_result(result, collector):
    df_ = pd.DataFrame(
        {
            "result": result,
            "timing_duration": collector.last.timing.duration_ms,
            "input_tokens": collector.last.usage.input_tokens,
            "output_tokens": collector.last.usage.output_tokens,
            "calls": collector.last.calls,
        }
    )
    return df_


async def main():
    print("Hello from baml-pdf-parsing!")

    # pdf_collector = Collector(name="pdf-collector")
    # pdf_df = await run_pdf_parsing(pdf_collector)
    # pdf_df.to_csv("pdf_results.csv", index=False)

    img_collector = Collector(name="img-collector")
    img_df = await run_img_parsing(img_collector)
    img_df.to_csv("img_results.csv", index=False)


if __name__ == "__main__":
    asyncio.run(main())
