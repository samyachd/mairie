// components/OrdinateurForm.tsx
import { useForm } from "react-hook-form";
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import { Label } from "@/app/components/ui/label";
import type { Agent } from "@/app/types";
import type { OrdinateurCreatePayload } from "@/app/services/ordinateur";

interface Props {
  agents: Agent[];
  onSubmit: (data: OrdinateurCreatePayload) => void;
  isPending?: boolean;
  defaultValues?: Partial<OrdinateurCreatePayload>;  // ← nouveau
  submitLabel?: string;                                // ← nouveau
}

export function OrdinateurForm({
  agents,
  onSubmit,
  isPending,
  defaultValues,
  submitLabel = "Créer l'ordinateur",
}: Props) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<OrdinateurCreatePayload>({
    defaultValues: {
      nom_reseau: defaultValues?.nom_reseau ?? "",
      marque: defaultValues?.marque ?? "",
      date_achat:
        defaultValues?.date_achat ?? new Date().toISOString().split("T")[0],
      proprietaire: defaultValues?.proprietaire ?? "",
      service: defaultValues?.service ?? "",
      agent_id: defaultValues?.agent_id ?? null,
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Label htmlFor="nom_reseau">Nom réseau *</Label>
        <Input
          id="nom_reseau"
          placeholder="ORD-006"
          {...register("nom_reseau", { required: "Le nom de réseau est obligatoire" })}
        />
        {errors.nom_reseau && (
          <p className="text-sm text-red-600 mt-1">{errors.nom_reseau.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="marque">Marque *</Label>
        <Input
          id="marque"
          placeholder="Dell"
          {...register("marque", { required: "La marque est obligatoire" })}
        />
        {errors.marque && (
          <p className="text-sm text-red-600 mt-1">{errors.marque.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="date_achat">Date d'achat *</Label>
        <Input
          id="date_achat"
          type="date"
          {...register("date_achat", { required: "La date est obligatoire" })}
        />
        {errors.date_achat && (
          <p className="text-sm text-red-600 mt-1">
            {errors.date_achat.message}
          </p>
        )}
      </div>

      <div>
        <Label htmlFor="proprietaire">Propriétaire</Label>
        <Input
          id="proprietaire"
          placeholder="Jean Dupont"
          {...register("proprietaire")}
        />
      </div>

      <div>
        <Label htmlFor="service">Service</Label>
        <Input id="service" placeholder="État Civil" {...register("service")} />
      </div>

      <div>
        <Label htmlFor="agent_id">Agent rattaché</Label>
        <select
          id="agent_id"
          className="w-full border rounded-md px-3 py-2 text-sm"
          {...register("agent_id", {
            setValueAs: (v) => (v === "" ? null : Number(v)),
          })}
        >
          <option value="">— Aucun —</option>
          {agents.map((agent) => (
            <option key={agent.id} value={agent.id}>
              {agent.prenom} {agent.nom} ({agent.service ?? "—"})
            </option>
          ))}
        </select>
      </div>

      <div className="flex justify-end pt-4">
        <Button type="submit" disabled={isPending}>
          {isPending ? "Enregistrement..." : submitLabel}
        </Button>
      </div>
    </form>
  );
}