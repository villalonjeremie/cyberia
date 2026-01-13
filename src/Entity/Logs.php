<?php

namespace App\Entity;

use App\Repository\LogsRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: LogsRepository::class)]
class Logs
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(nullable: true)]
    private ?array $logs_json = null;

    #[ORM\Column(length: 255)]
    private ?string $security_type = null;

    #[ORM\Column]
    private ?\DateTimeImmutable $created_at = null;

    #[ORM\Column]
    private ?bool $is_processed = null;

    public function __construct()
    {
        $this->created_at = new \DateTimeImmutable();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getLogsJson(): ?array
    {
        return $this->logs_json;
    }

    public function setLogsJson(?array $logs_json): static
    {
        $this->logs_json = $logs_json;

        return $this;
    }

    public function getSecurityType(): ?string
    {
        return $this->security_type;
    }

    public function setSecurityType(string $security_type): static
    {
        $this->security_type = $security_type;

        return $this;
    }

    public function getCreatedAt(): ?\DateTimeImmutable
    {
        return $this->created_at;
    }

    public function setCreatedAt(\DateTimeImmutable $created_at): static
    {
        $this->created_at = $created_at;

        return $this;
    }

    public function isProcessed(): ?bool
    {
        return $this->is_processed;
    }

    public function setIsProcessed(bool $is_processed): static
    {
        $this->is_processed = $is_processed;

        return $this;
    }
}
