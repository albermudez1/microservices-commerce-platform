<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Http;
use Throwable;

class ReportGatewayController extends Controller
{
    public function totalSales(): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $reportsServiceUrl = rtrim(env('REPORTS_SERVICE_URL', 'http://127.0.0.1:8002'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $headers = [
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ];

            $salesResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$salesServiceUrl}/api/sales");

            if ($salesResponse->failed()) {
                return response()->json($salesResponse->json(), $salesResponse->status());
            }

            $payload = [
                'sales' => $salesResponse->json(),
            ];

            $reportResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->post("{$reportsServiceUrl}/api/reports/total-sales", $payload);

            return response()->json(
                $reportResponse->json(),
                $reportResponse->status()
            );
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de reportes.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function salesByProduct(): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $reportsServiceUrl = rtrim(env('REPORTS_SERVICE_URL', 'http://127.0.0.1:8002'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $headers = [
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ];

            $salesResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$salesServiceUrl}/api/sales");

            if ($salesResponse->failed()) {
                return response()->json($salesResponse->json(), $salesResponse->status());
            }

            $payload = [
                'sales' => $salesResponse->json(),
            ];

            $reportResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->post("{$reportsServiceUrl}/api/reports/sales-by-product", $payload);

            return response()->json(
                $reportResponse->json(),
                $reportResponse->status()
            );
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de reportes.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function salesByUser(): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $reportsServiceUrl = rtrim(env('REPORTS_SERVICE_URL', 'http://127.0.0.1:8002'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $headers = [
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ];

            $salesResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$salesServiceUrl}/api/sales");

            if ($salesResponse->failed()) {
                return response()->json($salesResponse->json(), $salesResponse->status());
            }

            $payload = [
                'sales' => $salesResponse->json(),
            ];

            $reportResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->post("{$reportsServiceUrl}/api/reports/sales-by-user", $payload);

            return response()->json(
                $reportResponse->json(),
                $reportResponse->status()
            );
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de reportes.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

}
