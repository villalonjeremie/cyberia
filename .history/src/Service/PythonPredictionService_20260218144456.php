<?php

namespace App\Service;

use Symfony\Contracts\HttpClient\HttpClientInterface;

class PythonPredictionService
{
    private HttpClientInterface $client;
    private string $pythonApiUrl;
    private string $pythonApiKey;

    public function __construct(
        HttpClientInterface $client,
        string $pythonApiUrl,
        string $pythonApiKey
    ) {
        $this->client = $client;
        $this->pythonApiUrl = $pythonApiUrl;
        $this->pythonApiKey = $pythonApiKey;
    }

    public function sendLogFile(string $filePath): array
    {
        try {
            if (!file_exists($filePath)) {
                throw new \Exception("Fichier introuvable : $filePath");
            }

                            'contents' => fopen($filePath, 'r'),
            var_dump()

            $response = $this->client->request(
                'POST',
                $this->pythonApiUrl . '/predict',
                [
                    'headers' => [
                        'X-API-KEY' => $this->pythonApiKey,
                    ],

                    'multipart' => [
                        [
                            'name' => 'file',
                            'contents' => fopen($filePath, 'r'),
                            'filename' => basename($filePath),
                        ]
                    ],
                    'timeout' => 60,
                ]
            );

            return $response->toArray();

        } catch (\Throwable $e) {

            return [
                'status' => 'error',
                'message' => $e->getMessage(),
            ];
        }
    }

}
