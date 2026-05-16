import csv
from pathlib import Path
from datetime import datetime
import math

# fieldnames = [
#     "id", "filename", "width_init", "height_init", "width_inter", "height_inter", "width_res", "height_res", "interpolation", 
#     "scale", "scale_first", "scale_second", "mode", "model_name", "total_images", "time_ms", "mse", "psnr", "ssim",  "throughput"
# ]

excluded_keys = {"input_path", "output_path"}

class ResultManager:

    @staticmethod
    def export_csv(results, response_id):
        if not results:
            return

        mode = results[0].get("mode", "Unknown") if len(results) > 0 else "Unknown"

        run_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results_dir = Path("results") / "csv" #/ run_time
        results_dir.mkdir(parents=True, exist_ok=True)
        output_file = results_dir / f"results_{mode}_{run_time}.csv"

        fieldnames = ["id"] + [k for k in results[0].keys() if k not in excluded_keys]

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')

            writer.writeheader()

            for row in results:
                clean_row = row.copy()
                clean_row["id"] = response_id
            
                writer.writerow(clean_row)

        print(f"CSV saved to: {output_file}")
    
    def calculate_stats(self, key, results):
        values = [res[key] for res in results if not math.isnan(res.get(key, float('nan')))]
        if not values:
            return 0.0, 0.0, 0.0
        return min(values), sum(values) / len(values), max(values)
    
    def aggregate_results(self, results):
        aggregates = {}

        aggregates["time_min"], aggregates["time_avg"], aggregates["time_max"] = self.calculate_stats("time_ms", results)
        aggregates["mse_min"], aggregates["mse_avg"], aggregates["mse_max"] = self.calculate_stats("mse", results)
        aggregates["psnr_min"], aggregates["psnr_avg"], aggregates["psnr_max"] = self.calculate_stats("psnr", results)
        aggregates["ssim_min"], aggregates["ssim_avg"], aggregates["ssim_max"] = self.calculate_stats("ssim", results)
        aggregates["throughput_min"], aggregates["throughput_avg"], aggregates["throughput_max"] = self.calculate_stats("throughput", results)

        return aggregates