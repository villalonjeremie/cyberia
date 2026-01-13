<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Attribute\Route;
use Doctrine\ORM\EntityManagerInterface;
use App\Entity\Logs;

final class LogController
{
    #[Route('/api/log',name: 'api_log', methods: ['POST'])]
    public function __invoke(Request $request, EntityManagerInterface $em): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (!is_array($data)) {
            return new JsonResponse(
                ['error' => 'Invalid JSON'],
                400
            );
        }

        $logs = new Logs();
        $logs->setSecurityType($data['type']);
        $logs->setLogsJson($data['content']);
        $logs->setCreatedAt($logs->getCreatedAt());

        $em->persist($logs);
        $em->flush();

        return new JsonResponse([
            'status' => 'ok',
            'received' => $data,
        ]);
    }
}
