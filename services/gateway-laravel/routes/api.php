<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Services\ProductGatewayController;
use App\Http\Controllers\Services\SalesGatewayController;
use App\Http\Controllers\Services\RecommendationGatewayController;

Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);
Route::post('/reset-password', [AuthController::class, 'resetPassword']);

Route::middleware('auth:sanctum')->group(function () {
    # Gateway routes
    Route::get('/me', [AuthController::class, 'me']);
    Route::post('/logout', [AuthController::class, 'logout']);

    # Product routes
    Route::get('/products', [ProductGatewayController::class, 'index']);
    Route::get('/products/{id}', [ProductGatewayController::class, 'show']);
    Route::post('/products', [ProductGatewayController::class, 'store']);
    Route::put('/products/{id}', [ProductGatewayController::class, 'update']);
    Route::delete('/products/{id}', [ProductGatewayController::class, 'destroy']);
    Route::get('/products/{id}/stock', [ProductGatewayController::class, 'stock']);
    Route::patch('/products/{id}/stock/decrease', [ProductGatewayController::class, 'decreaseStock']);
    Route::patch('/products/{id}/stock/increase', [ProductGatewayController::class, 'increaseStock']);

    # Sale routes
    Route::get('/sales', [SalesGatewayController::class, 'index']);
    Route::get('/sales/{id}', [SalesGatewayController::class, 'show']);
    Route::post('/sales', [SalesGatewayController::class, 'store']);
    Route::get('/sales/user/{userId}', [SalesGatewayController::class, 'byUser']);
    Route::get('/sales/date-range/search', [SalesGatewayController::class, 'byDateRange']);
    Route::post('/sales/process', [SalesGatewayController::class, 'process']);

    # Recommendation routes
    Route::get('/recommendations/top-selling', [RecommendationGatewayController::class, 'topSelling']);
    Route::get('/recommendations/user', [RecommendationGatewayController::class, 'userRecommendations']);
    Route::get('/recommendations/price-max', [RecommendationGatewayController::class, 'priceMax']);

});
