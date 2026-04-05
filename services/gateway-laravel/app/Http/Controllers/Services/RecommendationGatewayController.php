<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Http;
use Throwable;

class RecommendationGatewayController extends Controller
{
    public function topSelling(): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $recommendationsServiceUrl = rtrim(env('RECOMMENDATIONS_SERVICE_URL', 'http://127.0.0.1:8001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $headers = [
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ];

            $productsResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$catalogServiceUrl}/api/products");

            if ($productsResponse->failed()) {
                return response()->json($productsResponse->json(), $productsResponse->status());
            }

            $salesResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$salesServiceUrl}/api/sales");

            if ($salesResponse->failed()) {
                return response()->json($salesResponse->json(), $salesResponse->status());
            }

            $payload = [
                'products' => $productsResponse->json(),
                'sales' => $salesResponse->json(),
            ];

            $recommendationsResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->post("{$recommendationsServiceUrl}/api/recommendations/top-selling", $payload);

            return response()->json(
                $recommendationsResponse->json(),
                $recommendationsResponse->status()
            );
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de recomendaciones.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function userRecommendations(): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $recommendationsServiceUrl = rtrim(env('RECOMMENDATIONS_SERVICE_URL', 'http://127.0.0.1:8001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');
        $user = request()->user();

        try {
            $headers = [
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ];

            $productsResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$catalogServiceUrl}/api/products");

            if ($productsResponse->failed()) {
                return response()->json($productsResponse->json(), $productsResponse->status());
            }

            $salesResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$salesServiceUrl}/api/sales");

            if ($salesResponse->failed()) {
                return response()->json($salesResponse->json(), $salesResponse->status());
            }

            $payload = [
                'userId' => $user->id,
                'products' => $productsResponse->json(),
                'sales' => $salesResponse->json(),
            ];

            $recommendationsResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->post("{$recommendationsServiceUrl}/api/recommendations/user", $payload);

            return response()->json(
                $recommendationsResponse->json(),
                $recommendationsResponse->status()
            );
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de recomendaciones.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function priceMax(): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $recommendationsServiceUrl = rtrim(env('RECOMMENDATIONS_SERVICE_URL', 'http://127.0.0.1:8001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');
        $maxPrice = request()->query('maxPrice');

        if ($maxPrice === null) {
            return response()->json([
                'message' => 'El parámetro maxPrice es obligatorio.',
            ], 400);
        }

        try {
            $headers = [
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ];

            $productsResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$catalogServiceUrl}/api/products");

            if ($productsResponse->failed()) {
                return response()->json($productsResponse->json(), $productsResponse->status());
            }

            $salesResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->get("{$salesServiceUrl}/api/sales");

            if ($salesResponse->failed()) {
                return response()->json($salesResponse->json(), $salesResponse->status());
            }

            $payload = [
                'maxPrice' => is_numeric($maxPrice) ? $maxPrice + 0 : $maxPrice,
                'products' => $productsResponse->json(),
                'sales' => $salesResponse->json(),
            ];

            $recommendationsResponse = Http::withHeaders($headers)
                ->timeout(10)
                ->post("{$recommendationsServiceUrl}/api/recommendations/price-max", $payload);

            return response()->json(
                $recommendationsResponse->json(),
                $recommendationsResponse->status()
            );
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de recomendaciones.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

}
