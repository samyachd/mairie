import { useForm } from "react-hook-form";
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import { Label } from "@/app/components/ui/label";
import type { UserCreatePayload, UserUpdatePayload } from "@/app/services/user";

type FormValues = {
  nom: string;
  email: string;
  password: string;
  role: "admin" | "user" | "read";
};

interface Props {
  onSubmit: (data: UserCreatePayload | UserUpdatePayload) => void;
  isPending?: boolean;
  defaultValues?: Partial<FormValues>;
  isEdit?: boolean;
}

const ROLES: { value: FormValues["role"]; label: string }[] = [
  { value: "admin",  label: "Administrateur" },
  { value: "user",   label: "Utilisateur" },
  { value: "read",   label: "Lecture seule" },
];

const PASSWORD_HINT = "8 car. min., majuscule, minuscule, chiffre, caractère spécial (@$!%*?&)";

export function UserForm({ onSubmit, isPending, defaultValues, isEdit = false }: Props) {
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({
    defaultValues: {
      nom:      defaultValues?.nom      ?? "",
      email:    defaultValues?.email    ?? "",
      password: "",
      role:     defaultValues?.role     ?? "read",
    },
  });

  const handleValid = (data: FormValues) => {
    if (isEdit) {
      const payload: UserUpdatePayload = {
        nom:   data.nom   || undefined,
        email: data.email || undefined,
        role:  data.role  || undefined,
      };
      if (data.password) payload.password = data.password;
      onSubmit(payload);
    } else {
      onSubmit(data as UserCreatePayload);
    }
  };

  return (
    <form onSubmit={handleSubmit(handleValid)} className="space-y-4">
      <div>
        <Label htmlFor="nom">Nom *</Label>
        <Input
          id="nom"
          placeholder="Jean Dupont"
          {...register("nom", { required: !isEdit && "Le nom est obligatoire" })}
        />
        {errors.nom && <p className="text-sm text-red-600 mt-1">{errors.nom.message}</p>}
      </div>

      <div>
        <Label htmlFor="email">Email *</Label>
        <Input
          id="email"
          type="email"
          placeholder="jean.dupont@mairie.fr"
          {...register("email", { required: !isEdit && "L'email est obligatoire" })}
        />
        {errors.email && <p className="text-sm text-red-600 mt-1">{errors.email.message}</p>}
      </div>

      <div>
        <Label htmlFor="password">
          Mot de passe {isEdit ? <span className="text-muted-foreground font-normal">(laisser vide pour ne pas changer)</span> : "*"}
        </Label>
        <Input
          id="password"
          type="password"
          placeholder={isEdit ? "••••••••" : "Nouveau mot de passe"}
          {...register("password", { required: !isEdit && "Le mot de passe est obligatoire" })}
        />
        <p className="text-xs text-muted-foreground mt-1">{PASSWORD_HINT}</p>
        {errors.password && <p className="text-sm text-red-600 mt-1">{errors.password.message}</p>}
      </div>

      <div>
        <Label htmlFor="role">Rôle *</Label>
        <select
          id="role"
          {...register("role")}
          className="w-full h-9 border rounded px-3 text-sm bg-white"
        >
          {ROLES.map((r) => (
            <option key={r.value} value={r.value}>{r.label}</option>
          ))}
        </select>
      </div>

      <div className="flex justify-end pt-2">
        <Button type="submit" disabled={isPending}>
          {isPending ? "Enregistrement…" : isEdit ? "Enregistrer" : "Créer l'utilisateur"}
        </Button>
      </div>
    </form>
  );
}
