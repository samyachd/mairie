import { useForm } from "react-hook-form";
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import { Label } from "@/app/components/ui/label";
import type { AgentPayload } from "@/app/services/agent";

interface Props {
  onSubmit: (data: AgentPayload) => void;
  isPending?: boolean;
  defaultValues?: Partial<AgentPayload>;
  submitLabel?: string;
}

export function AgentForm({
  onSubmit,
  isPending,
  defaultValues,
  submitLabel = "Créer l'agent",
}: Props) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<AgentPayload>({
    defaultValues: {
      nom: defaultValues?.nom ?? "",
      prenom: defaultValues?.prenom ?? "",
      service: defaultValues?.service ?? "",
      email: defaultValues?.email ?? "",
      telephone: defaultValues?.telephone ?? "",
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="prenom">Prénom *</Label>
          <Input
            id="prenom"
            placeholder="Jean"
            {...register("prenom", { required: "Le prénom est obligatoire" })}
          />
          {errors.prenom && (
            <p className="text-sm text-red-600 mt-1">{errors.prenom.message}</p>
          )}
        </div>

        <div>
          <Label htmlFor="nom">Nom *</Label>
          <Input
            id="nom"
            placeholder="Dupont"
            {...register("nom", { required: "Le nom est obligatoire" })}
          />
          {errors.nom && (
            <p className="text-sm text-red-600 mt-1">{errors.nom.message}</p>
          )}
        </div>
      </div>

      <div>
        <Label htmlFor="service">Service</Label>
        <Input
          id="service"
          placeholder="État Civil"
          {...register("service")}
        />
      </div>

      <div>
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="jean.dupont@mairie.fr"
          {...register("email", {
            pattern: {
              value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
              message: "Format d'email invalide",
            },
          })}
        />
        {errors.email && (
          <p className="text-sm text-red-600 mt-1">{errors.email.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="telephone">Téléphone</Label>
        <Input
          id="telephone"
          type="tel"
          placeholder="01 23 45 67 89"
          {...register("telephone")}
        />
      </div>

      <div className="flex justify-end pt-4">
        <Button type="submit" disabled={isPending}>
          {isPending ? "Enregistrement..." : submitLabel}
        </Button>
      </div>
    </form>
  );
}